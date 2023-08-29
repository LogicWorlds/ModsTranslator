
import sys, argparse
from translate_app.FileWorker import FileWorker
from translate_app.TranslateUtils import TranslateUtils
from translate_app.Utils import Utils

# Handle params
argParser = argparse.ArgumentParser()
argParser.add_argument("-fl", "--from_lang", help="translate from language", default="en")
argParser.add_argument("-tl", "--to_lang", help="translate to language", default="ru")
argParser.add_argument("-p", "--patch_mod", help="include translation in mods", action="store_true")
argParser.add_argument("--debug", help="enable debug output", default=False, action="store_true")
argParser.add_argument("PATH", help="path to mods folder") # C:\PrismMC\instances\BioTech\.minecraft\mods
args = argParser.parse_args()


fw = FileWorker()
tu = TranslateUtils()
utils = Utils()
tu.debug = args.debug
# Get all mods and their languages
mods = fw.scan_mods_dir(args.PATH)
for mod in mods:
    mod_file = mod['mod_file']
    mod_langfiles = mod['lang_files']
    mod_file_path = f"{args.PATH}/{mod_file}"
    has_first_lang = fw.has_lang_file(mod_langfiles, args.from_lang)
    has_second_lang = fw.has_lang_file(mod_langfiles, args.to_lang)
    
    if args.debug: print(mod)
    
    # Check lang files exist
    if has_second_lang:
        # If required language is available - skip this mod
        print(f"{mod_file.ljust(50)}-> Mod has {args.to_lang.upper()} lang (Skipping)")
        continue
    if not has_first_lang:
        print(f"{mod_file.ljust(50)}-> Mod does have {args.from_lang.upper()} lang (Skipping)...")
        continue
    
    # Start translation mod
    print(f"{mod_file.ljust(50)}-> Translating...") 

    # Get lang file data
    first_lang_path = fw.get_lang_file_path(mod_langfiles, args.from_lang)
    lang_file_data_from = fw.get_lang_file_data(mod_file_path, first_lang_path)

    # Check format of lang
    format = 'lang'
    if utils.is_json(lang_file_data_from): format = 'json'

    # Translate lang
    translated_data = tu.translate(lang_file_data_from, args.to_lang, data_type=format)
    
    # Save file (separately or included in the mod)
    fw.save_lang_file(mod_langfiles, mod_file_path, translated_data, format, args.to_lang, args.patch_mod)
