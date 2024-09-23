from easygoogletranslate import EasyGoogleTranslate
import json


class TranslateUtils(object):
    debug = False

    def __init__(self) -> None:
        pass

    def translate(self, data, to_lang, data_type="default") -> str:
        # Check format of lang
        if data_type == "json":
            return self.translate_json(data, to_lang)
        else:  # Old format name=value
            return self.translate_default(data, to_lang)

    def translate_by_translator(self, data, lang):
        gt = EasyGoogleTranslate()
        translated = ""
        to_translate_text = ""
        to_translate_packets = []

        # Prepare the packets for translation (max 5000 characters per packet)
        for line in data.splitlines():
            if (len(to_translate_text) + len(line)) > 3000:
                # If packet contains more than 4500 characters - add to packet and create new packet
                to_translate_packets.append(to_translate_text)
                to_translate_text = ""
            to_translate_text += f"{line}\n"

        # Add latest data to the last package
        if len(to_translate_text) > 0:
            to_translate_packets.append(to_translate_text)

        if self.debug:
            print(f"Translating...")
        for packet_id, to_translate_packet in enumerate(to_translate_packets):
            print(f"Translating packet: {str(packet_id+1)}")
            try:
                translated += "\n" + gt.translate(
                    to_translate_packet, target_language=lang
                )
            except Exception as e:
                print("===ERR===", to_translate_packet)
                print(e)

        return translated

    def translate_default(self, data, to_lang) -> str:
        translated = ""
        to_translated_text = ""
        # Preparing to translate...
        # Split and read line by line
        data_splited = data.split("\n")
        for data_line in data_splited:
            line_part = data_line.split("=")
            if len(line_part) > 1:
                # Add line to translation data (by new line)
                to_translated_text += "\n" + line_part[1]

        # Translate by translator
        to_translated_text = self.translate_by_translator(to_translated_text, to_lang)
        if self.debug:
            print(f"Compiling translated file...")
        to_translated_text = to_translated_text.split("\n")
        # For empty lines, comments we separatelycount the lines that need to be filled
        translated_line = 1
        # Place translated lines and assemble data to output
        for data_line in data_splited:
            line_part = data_line.split("=")
            label = line_part[0]
            if len(line_part) > 1:
                # Line with translation
                translated += f"{label}={to_translated_text[translated_line]}\n"
                translated_line += 1
            else:
                # Line without translation
                translated += f"{label}\n"
        return translated

    def translate_json(self, data, to_lang) -> str:
        data_list = json.loads(data)
        to_translate = ""
        for value in data_list:
            to_translate += "\n" + data_list[value]
        translated_text = self.translate_by_translator(to_translate, to_lang)

        # Place translated lines and assemble data to output
        translated_text = translated_text.split("\n")
        for i, value in enumerate(data_list):
            data_list[value] = translated_text[i + 1]
        data_list = json.dumps(data_list)  # , ensure_ascii=False
        return data_list
