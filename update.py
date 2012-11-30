import lxml.etree
import mechanize
import os
import os.path
import shutil
import sys
import tempfile

def download_profiles(account, password, dst_dir):
    BASE_URL = 'https://developer.apple.com'
    PORTAL_PATH = '/ios/manage/overview/index.action'
    DEV_PATH = '/ios/manage/provisioningprofiles/index.action'
    DISTRIB_PATH = '/ios/manage/provisioningprofiles/viewDistributionProfiles.action'

    def profile_file_path(profile_name):
        return os.path.join(dst_dir, profile_name + '.mobileprovision')

    def each_profile(profiles_path):
        parser = lxml.etree.HTMLParser(encoding='utf-8')
        tree = lxml.etree.fromstring(content, parser)
        for element in tree.xpath('//fieldset[@id="fs-0"]/table/tbody/tr'):
            names = element.xpath('td[@class="profile"]/a/span/text()')
            urls = element.xpath('td[@class="action"]/a[@id="remove_"]/@href')
            if len(names) > 0 and len(urls) > 0:
                yield(names[0], urls[0])

    browser = mechanize.Browser()

    # Login
    portal_url = BASE_URL + PORTAL_PATH
    response = browser.open(portal_url)
    if response.code != 200:
        raise IOError('Could not open login page')
    browser.select_form('appleConnectForm')
    browser['theAccountName'] = account
    browser['theAccountPW'] = password
    response = browser.submit()
    if response.code != 200 or response.geturl() != portal_url:
        raise IOError('Could not submit login page')

    # Look at development and distribution profiles
    for profiles_path in [DEV_PATH, DISTRIB_PATH]:
        response = browser.open(BASE_URL + profiles_path)
        if response.code != 200:
            raise IOError('Could not open profiles')
        content = response.read()
        for name, url in each_profile(content):
            browser.retrieve(BASE_URL + url, profile_file_path(name))

def replace_profiles(account, password):
    PROFILES_DIR = os.path.expanduser('~/Library/MobileDevice/Provisioning Profiles/')
    tmp_dir = tempfile.mkdtemp()
    try:
        download_profiles(account, password, tmp_dir)
        for old_profile in os.listdir(PROFILES_DIR):
            os.remove(os.path.join(PROFILES_DIR, old_profile))
        for new_profile in os.listdir(tmp_dir):
            shutil.copy(os.path.join(tmp_dir, new_profile), PROFILES_DIR)
    finally:
        shutil.rmtree(tmp_dir, True)

def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s <Apple ID> <Password>\n" % (sys.argv[0]))
        exit(1)
    replace_profiles(sys.argv[1], sys.argv[2])
    exit(0)

if __name__ == "__main__":
    main()
