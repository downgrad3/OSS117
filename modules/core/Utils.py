import logging, random, setting
from logging.handlers import RotatingFileHandler


class File:
    @staticmethod
    def write_in_txt(tab_elements, file_name):
        f_in = open(file_name, "w")
        for element in tab_elements:
            f_in.write(element + "\n")
        f_in.close()

    @staticmethod
    def write_in_csv(tab_elements, file_name):
        f_in = open(file_name, "w")
        for element in tab_elements:
            f_in.write(element + "\n")
        f_in.close()

    @staticmethod
    def get_from_file(file_name):
        tab_elements = []
        file = open(file_name, "r")
        for line in file.readlines():
            tab_elements.append(line.strip())
        file.close()

        return tab_elements


class Logger:

    @staticmethod
    def initialize_logger(logger_name, path):
        logger = logging.getLogger(logger_name)
        if not len(logger.handlers):
            formatter = logging.Formatter("%(asctime)s [%(levelname)s][%(threadName)s,%(filename)s:%(lineno)d] %(funcName)s(), %(message)s")

            handler_critic = logging.handlers.RotatingFileHandler(path + "/" + logger_name + "_warning.log", mode="a", maxBytes=10 * 1024 * 1024, backupCount=1, encoding="utf-8")
            handler_critic.setFormatter(formatter)
            handler_critic.setLevel(logging.WARNING)

            handler_info = logging.handlers.RotatingFileHandler(path + "/" + logger_name + "_debug.log", mode="a", maxBytes=10 * 1024 * 1024, backupCount=1, encoding="utf-8")
            handler_info.setFormatter(formatter)
            handler_info.setLevel(logging.DEBUG)

            logger.addHandler(handler_critic)
            logger.addHandler(handler_info)
            logger.setLevel(logging.DEBUG)

        return logger


class Oss117:

    @staticmethod
    def print_banner():
        quotes = [
            "Comment est votre blanquette ?"
            "Les plats a base de viandes, sont-il de bonne qualite ?",
            "Quand une femme change d'homme, elle change de coiffure",
            "J'aime me beurrer la biscotte.",
            "J'aime me battre.",
            "C'est quand même bien mieux une voiture propre ! ",
            "C'est notre Raïs à nous : c'est M.René Coty. Un grand homme. Il marquera l'Histoire.",
            "Il s'agirait de grandir ... il s'agirait de grandir",
            "Tu n'es pas seulement un lâche mais aussi un traitre, comme ta petite taille le laissait deviner !",
            "Ahahah. Ce bon vieux Bill !",
            "Oui je ... je connais cette theorie.",
            "On en reparlera quand il faudra porter quelque chose de lourd",
            "C'est l'inexpugnable arrogance de votre beauté qui m'asperge.",
            "Le mystère des Pyramides, c'est le mystère de la conscience dans laquelle on n'entre pas",
            "Des scientifiques font des experiences sur les mouches drosophiles parce que la structure de leur cerveau est extrêmement proche de la notre.",
            "Le cheval nous voit plus grand que nous sommes avec son oeil deformant. Ce n'est que grace a cela que nous l'avons domestique.",
            "Si le chat a la queue verticale, c'est qu'il est en confiance.",
            "23 à 0 ! C'est la piquette Jack ! Tu sais pas jouer Jack ! T'es mauvais !",
            "J'aime quand une jolie femme brune m'apporte mon petit déjeuner au lit"
        ]

        quote = random.choice(quotes)
        quote_len = len(quote)
        print("-" * (quote_len + 6))
        print("|| " + quote + " ||")
        print("-" * (quote_len + 6))

        print(" " * (quote_len - 7) + "\\")
        print(" " * (quote_len - 6) + "(◕_◕)╦╤─ ҉ ~ •")

    @staticmethod
    def check_mandatories_var_in_config_file(moduletype, mandatories_var, logger):
        # Testing if all mandatories variables are correctly set in the config.ini
        collectors_cfg = setting.config[moduletype]
        if not all(elem in collectors_cfg for elem in mandatories_var):
            logger.critical('Missing variables for the linkedin crawler, please review your config file. Mandatories variables are: ' + str(mandatories_var))
            print("Missing variables for the linkedin crawler, please review your config file. Mandatories variables are:" + str(mandatories_var))
            exit(1)