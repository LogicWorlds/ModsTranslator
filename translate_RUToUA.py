import sys, time
from yandexfreetranslate import YandexFreeTranslate
yt = YandexFreeTranslate()

if __name__ == "__main__":
    if len (sys.argv) == 1:
        print ("Привет, мир!")
    else:
        if len (sys.argv) < 3:
            print ("Ошибка. Слишком мало параметров.")
            sys.exit (1)

        #if len (sys.argv) > 3:
        #    print ("Ошибка. Слишком много параметров.")
        #    sys.exit (1)

        param_name = sys.argv[1]
        param_value = sys.argv[2]
        lang_from = 'ru'
        lang_to = 'uk'
        if len (sys.argv) > 3:
            lang_from = sys.argv[3]
            print('LEN-A')
        if len (sys.argv) > 4:
            lang_to = sys.argv[4]
            print('LEN-B')
        
        if (param_name == "--input" or
                param_name == "-i"):
            print ("Переводим: {}!".format (param_value) )
        else:
            print ("Ошибка. Неизвестный параметр '{}'".format (param_name) )
            sys.exit (1)

        try:
            f = open(param_value, encoding="utf-8")
            data = f.read();
            translated = ""
            line_number = 0
            # Разбиваем и читаем по строкам
            data_splited = data.split("\n")
            for data_line in data_splited:
                line_number += 1
                line_part = data_line.split("=")
                if (len(line_part) > 1):
                    label = line_part[0]
                    text = line_part[1]
                    translated_text = ""
                    if text:
                        translated_text = yt.translate(lang_from, lang_to, text)
                    translated_text = translated_text.replace('% ', '%')
                    translated_text = translated_text.replace('$ ', '$')
                    translated += f"{label}={translated_text}\n"
                    print(f"[{line_number}/{len(data_splited)}]: {translated_text}")
                    time.sleep(0.1)
                else:
                    label = line_part[0]
                    translated += f"{label}\n"



            ua_file_loc = param_value.replace('ru_RU', 'uk_UA')
            ua_file_loc = ua_file_loc.replace('ru_ru', 'uk_ua')
            t = open(ua_file_loc, "w", encoding="utf-8")
            t.write(translated)
            t.close()
            # Do something with the file
        except IOError:
            print("File not accessible")
        finally:
            f.close()
