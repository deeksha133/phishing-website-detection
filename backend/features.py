import urllib.parse
import re

class FeatureExtractor:
    def __init__(self, url):
        self.url = url
        if not re.match(r'^https?://', url):
            url_with_scheme = 'http://' + url
        else:
            url_with_scheme = url
            
        self.parsed = urllib.parse.urlparse(url_with_scheme)
        self.path = self.parsed.path
        self.domain = self.parsed.netloc
        
        # Normalize domain: remove 'www.' if present
        if self.domain.startswith('www.'):
            self.domain = self.domain[4:]
            
        self.file = self.path.split('/')[-1] if '/' in self.path else ''
        self.directory = self.path.rsplit('/', 1)[0] if '/' in self.path else ''

    def extract(self):
        features = {}
        
        # URL based features
        features['length_url'] = len(self.url)
        features['qty_slash_url'] = self.url.count('/')
        
        # Domain based features
        features['domain_length'] = len(self.domain)
        features['qty_dot_domain'] = self.domain.count('.')
        features['qty_vowels_domain'] = len([c for c in self.domain if c in 'aeiouAEIOU'])
        features['qty_digits_domain'] = len([c for c in self.domain if c.isdigit()])
        
        # Directory based features
        features['directory_length'] = len(self.directory)
        features['qty_slash_directory'] = self.directory.count('/')
        features['qty_underline_directory'] = self.directory.count('_')
        features['qty_dollar_directory'] = self.directory.count('$')
        features['qty_at_directory'] = self.directory.count('@')
        
        # File based features
        features['file_length'] = len(self.file)
        features['qty_dot_file'] = self.file.count('.')
        features['qty_underline_file'] = self.file.count('_')
        features['qty_equal_file'] = self.file.count('=')
        features['qty_questionmark_file'] = self.file.count('?')
        features['qty_and_file'] = self.file.count('&')
        features['qty_exclamation_file'] = self.file.count('!')
        features['qty_space_file'] = self.file.count(' ')
        features['qty_tilde_file'] = self.file.count('~')
        features['qty_comma_file'] = self.file.count(',')
        features['qty_plus_file'] = self.file.count('+')
        features['qty_asterisk_file'] = self.file.count('*')
        features['qty_hashtag_file'] = self.file.count('#')
        features['qty_dollar_file'] = self.file.count('$')
        features['qty_percent_file'] = self.file.count('%')

        return features

    @staticmethod
    def get_feature_names():
        return [
            'length_url', 'qty_slash_url',
            'domain_length', 'qty_dot_domain', 'qty_vowels_domain',
            'directory_length', 'qty_slash_directory', 'qty_underline_directory', 
            'qty_dollar_directory', 'qty_at_directory',
            'file_length', 'qty_dot_file', 'qty_underline_file', 'qty_equal_file',
            'qty_questionmark_file', 'qty_and_file', 'qty_exclamation_file',
            'qty_space_file', 'qty_tilde_file', 'qty_comma_file', 'qty_plus_file',
            'qty_asterisk_file', 'qty_hashtag_file', 'qty_dollar_file', 'qty_percent_file'
        ]
