import os, re, zipfile

NAME = 'FileWorker'

class FileWorker(object):
    lang_keys = {
        'en': 'en_us',
        'ru': 'ru_ru',
        'uk': 'uk_ua'
    }
    def __init__(self) -> None:
        pass

    def scan_mods_dir(self, path) -> list:
        # Scan the directory and get lang files
        result_data = []
        for mod in os.listdir(path):
            mod_path = f"{path}/{mod}";
            if (zipfile.is_zipfile(mod_path)):
                with zipfile.ZipFile(mod_path) as mod_file:
                    # Search lang files
                    mod_list_files = mod_file.namelist()
                    mod_lang_files = []
                    for mod_file_path in mod_list_files:
                        mfpl = mod_file_path.lower()
                        if mfpl.endswith(".lang") or re.search(r"\/lang.*\.json$", mfpl):
                            mod_lang_files.append(mod_file_path)  
                    # Add to result mod_file and all lang files 
                    result_data.append({'mod_file':mod,
                                        'lang_files': mod_lang_files})
        return result_data
    
    def convert_lang_format(self, lang_key) -> str:
        # Converting formats (eg. en -> en_us)
        if lang_key in self.lang_keys:
            return self.lang_keys[lang_key]
    
    def has_lang_file(self, list_langs, lang_key) -> bool:
        lang_key = self.convert_lang_format(lang_key)
        # Search file in list of languages
        for lang_file in list_langs:
            # Lowercase all file names for correct searching
            lfl = lang_file.lower()
            if lfl.endswith(f"{lang_key}.lang") or lfl.endswith(f"{lang_key}.json"):
                # Return true if lang_file is in list of languages
                return True
        # Return false if lang_file is not in list of languages
        return False
    
    def get_lang_file_path(self, list_langs, lang) -> str:
        lang = self.convert_lang_format(lang)
        # Search file in list of languages
        for lang_file in list_langs:
            lfl = lang_file.lower()
            if lfl.endswith(f"{lang}.lang") or lfl.endswith(f"{lang}.json"):
                # Return file path
                return lang_file
    
    def get_lang_file_data(self, mod_file_path, lang_file_path):
        with zipfile.ZipFile(mod_file_path) as mod_f:
            with mod_f.open(lang_file_path) as lang_file:
                return lang_file.read().decode('UTF-8')
    
    def save_lang_file(self, list_langs, mod_file_path, 
                       data, format, lang, include_in_mod = False) -> bool:
        lang_file_name = self.convert_lang_format(lang)+"."+format
        path_to_langs = os.path.dirname(list_langs[0])
        path_to_write = f"{path_to_langs}/{lang_file_name}"
        if include_in_mod:
            with zipfile.ZipFile(mod_file_path, 'a') as mod_f:
                data = str.encode(data)
                mod_f.writestr(path_to_write, data)
        else:
            res_dir = os.getcwd()+"/resources/"
            os.makedirs(res_dir+path_to_langs, exist_ok=True)
            with open(res_dir+path_to_write, "w") as f:
                f.write(data)
        return True
            