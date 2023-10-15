from httpx import Response
from utils.parser import get_response_as_dict


class LoadData:

    def get_value(self, response: Response, key: str) -> str | int:
        """Getting the value from the answer by key name"""
        response_as_dict = get_response_as_dict(response)
        return response_as_dict.get(key)

    def load_translation(self, locale: str) -> str:
        """Getting the value in the "description" key by locale"""
        translation = {
            "RU": "Трясенье До Кровавые утоленье От не На их то ах. Освещенных сокровищей устремится. Громады ведущий рог Все Покроет вид ров том Парящий выходил. Ней Тем при хор Лук здешня другие Злобны слезна Оне мне. Чья тощ там уха чтя Лук. Им Парки уж сидят ей Хвали Слова от Ее всюды НА. . Твое став хотя.",
            "EN": "Ye on properly handsome returned throwing am no whatever. In without wishing he of picture no exposed talking minutes. Curiosity continual belonging offending so explained it exquisite. Do remember to followed yourself material mr recurred carriage. High drew west we no or at john. About or given on witty event. Or sociable up material bachelor bringing landlord confined. Busy so many in hung easy find well up. So of exquisite my an explained remainder. Dashwood denoting securing be on perceive my laughing so.",
            "PL": "Podkomorzynę powróciłaś tonąc spadku Lombardskiém kutasy dumać. Tonąc trzech kolną tajnym. Rozum żył rosciągnionych licem sądu rosciągnionemi Przysiągłbyś Otoż chowa niepowiedziała Runie Bezładnością Dobre. Podziękować okna nogi ojca Przyjechawszy byle przysunąwszy światłość domy. Pijem mniej gniew znów dziwi ruszy Żyje."
        }
        return translation.get(locale)


load_data = LoadData()
