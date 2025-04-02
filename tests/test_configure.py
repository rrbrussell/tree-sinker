import configparser
import sys

def test_configuration():
    config = configparser.ConfigParser()
    config['fetch from'] = {'server': 'https://server.example.com', 'path': '/directory1/directory2'}
    config['store into'] = {'repos_dir': '/var/db/repos'}
    config.read('./etc/tree-sinker.ini')
    assert 'fetch from' in config
    #assert that our default values were overwritten
    assert config['fetch from']['server'] != 'https://server.example.com'
    assert config['fetch from']['server'] == 'http://server.example.com'
    assert 'path' in config['fetch from']
    assert 'store into' in config
    assert 'repos_dir' in config['store into']

#End of buffer
