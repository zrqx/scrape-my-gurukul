# scrape-my-gurukul

**Scrape Student data from my-gurukul.com**

## Disclaimer
Should strictly be used for Educational and/or Exploration purposes.
You shall not misuse this tool to gain unauthorised access. The author will not be held responsible in the event any charges be brought against any individuals misusing the tool to break the law.

## Installation and Setup
- Python3 and pip3 are prerequisites
- Install latest version of Firefox Web Browser

    ```bash
    sudo apt-get install firefox
    ```
- Download the Latest version of Geckodriver
    ```
    git clone https://github.com/zrqx/scrape-my-gurukul.git
    ```

    ```
    cd scrape-my-gurukul && mkdir drivers
    ```

    ```
    url=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | python3 -c "import sys, json; print(next(item['browser_download_url'] for item in json.load(sys.stdin)['assets'] if 'linux64' in item.get('browser_download_url', '')))")
    ```

    ```
    wget -i $url -P drivers/
    ```

    ```
    tar -xvf geckodriver*.tar.gz -C drivers/ && rm -f geckodriver*.tar.gz
    ```
- Install all the dependencies
    ```bash
    pip3 install requirements.txt
    ```

## Usage

```bash
python3 scrapy.py -u USN -p PASSWORD
```
USN & PASSWORD should be replaced with respective values.

The program returns prints json data to the stdout, which can be redirected to file

```
python3 scrapy.py -u USN -p PASSWORD > hello.json
```
### Tested on Elementary OS 5.1.7 Hera (Builtz on Ubuntu 18.04.4 LTS)

