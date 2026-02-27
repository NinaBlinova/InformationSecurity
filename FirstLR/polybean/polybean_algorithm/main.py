from enum import Enum
from pprint import pprint
from typing import Optional

from FirstLR.polybean.polybean_algorithm.utils import *
from FirstLR.polybean.polybean_algorithm.utils.frequency_analysis_new import FrequencyAnalysisNew


def key_accuracy(original_key_matrix, hacked_key) -> float:
    total = 0
    matches = 0
    for i in range(min(len(original_key_matrix), len(hacked_key))):
        for j in range(min(len(original_key_matrix[i]), len(hacked_key[i]))):
            if original_key_matrix[i][j] != '*':
                total += 1
                if original_key_matrix[i][j] == hacked_key[i][j]:
                    matches += 1
    print(matches)
    print(total)
    if total == 0:
        return 0.0

    return matches / total * 100


class Command(Enum):
    EXIT = '0'

    DELETE_KEY = '1'
    INPUT_KEY = '2'
    GENERATE_KEY = '3'

    ENCRIPT = '4'
    DECRIPT = '5'
    FREQUENCY_ANALYSIS = '6'

    NOTHING = '7'

    @classmethod
    def _missing_(cls, value):
        return cls.NOTHING


class Main:
    __slots__ = ('command', 'polybean_cipher')

    def __init__(self):
        self.polybean_cipher: Optional[PolybeanCipher] = None
        self.command = Command.NOTHING

    def draw_menu(self):
        print('0 - exit')
        if self.polybean_cipher is not None:
            print('1 - delete key')
            print('4 - encrypt')
            print('5 - decrypt')
        else:
            print('2 - input key')
            print('3 - generate random key')
        print('6 - frequence analysis')

    def delete_key(self):
        self.polybean_cipher = None

    def input_key(self):
        print("Enter key (finish with empty line):")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)

        key_input = "\n".join(lines)

        try:
            key = create_key_matrix_from_text(key_input)
            self.polybean_cipher = PolybeanCipher(key)
        except Exception:
            print('Invalid key')

    def generate_key(self):
        key = get_random_key()
        print_key_matrix(key)
        self.polybean_cipher = PolybeanCipher(key)

    def encrypt(self):
        message = input('Enter message: ')
        try:
            encrypted_message = self.polybean_cipher.encrypt(message)
            print(encrypted_message)
        except Exception:
            print('Invalid message')

    def decrypt(self):
        message = input('Enter message: ')
        try:
            decrypted_message = self.polybean_cipher.decrypt(message)
            print(decrypted_message)
        except Exception:
            print('Invalid message')

    def frequence_analysis(self):
        message = input('Enter message: ')
        try:
            frequency_analysis = FrequencyAnalysis(message)
            frequency_analysis.print_table()
            frequency_analysis.print_possible_text()
            key = frequency_analysis.get_restored_key()
            print(key)
            original_key = self.polybean_cipher._key_matrix
            accuracy = key_accuracy(original_key, key)
            print(f"\nKey совпадение: {accuracy:.2f}%")
        except Exception:
            print('Invalid message')

    def run(self):
        while self.command != Command.EXIT:
            match self.command:
                case Command.DELETE_KEY:
                    self.delete_key()
                case Command.INPUT_KEY:
                    self.input_key()
                case Command.GENERATE_KEY:
                    self.generate_key()
                case Command.ENCRIPT:
                    self.encrypt()
                case Command.DECRIPT:
                    self.decrypt()
                case Command.FREQUENCY_ANALYSIS:
                    self.frequence_analysis()

            self.draw_menu()
            self.command = Command(input('Enter command: '))


if __name__ == '__main__':
    main = Main()
    main.run()

"""
theforestawakenswiththefirstraysofsunlightfilteringthroughthecanopyabovetheairisfilledwiththefreshscentofpineandearthafteranovernightrainbirdsbeginchirpinggreetingthedaywiththeirsongsasasoftbreezerustlestheleavescreatingagentlemelodythatechosthroughthetreesabeautifuldeerstepslightlyoverthemosscoveredgrounditsgracefulmovementsbarelydisturbingthesilencebelowabrookflowsoverpolishedstonesitscrystalclearwatersparklinginthemorninglightthisisasacredplacefulloflifewheretimemovesmoreslowlyandthehustleoftheoutsideworldseemsadistantmemoryeverybreathfeelslikeameditationandthesoulfindsapeaceimpossibletoachieveelsewhereherenatureremindsusofitstimelessbeautyandpower
mtnymgzymuntmgatmtzgnfzgzumgauatnfaymtnymtnymgzyayntatmtntzgmfatmuzyatzfaupuaypynymtzyaypumtmgntayaupymtnyntmuzfpynymtnymgngzgaumuztmfzgpgmupfmgmtnymgzgayntayatzyaypupumgagnfaymtnymtnymgzyntmgatnyatngmgaumtmuzyztayaumgzgauagmgzgntmtnyzgzymtmgntzgaumupfmgntauaypynymtntzgayaupgayntagatpgmgpyayaungnyayntztayaupypyntmgmgmtayaupymtnymgagzgmfnfaymtnymtnymgayntatmuaupyatzgatzgatmuzymtpgntmgmgzqmgntzfatmtpumgatmtnymgpumgzgpfmgatngntmgzgmtayaupyzgpymgaumtpumgnumgpumuagmfmtnyzgmtmgngnymuatmtnyntmuzfpynymtnymgmtntmgmgatzgpgmgzgzfmtayzyzfpuagmgmgntatmtmgztatpuaypynymtpumfmupfmgntmtnymgnumuatatngmupfmgntmgagpyntmuzfauagaymtatpyntzgngmgzyzfpunumupfmgnumgaumtatpgzgntmgpumfagayatmtzfntpgayaupymtnymgataypumgaungmgpgmgpumunfzgpgntmumuzuzypumunfatmupfmgntztmupuayatnymgagatmtmuaumgataymtatngntmfatmtzgpungpumgzgntnfzgmtmgntatztzgntzupuayaupyayaumtnymgnumuntauayaupypuaypynymtmtnyayatayatzgatzgngntmgagztpuzgngmgzyzfpupumuzypuayzymgnfnymgntmgmtaynumgnumupfmgatnumuntmgatpumunfpumfzgauagmtnymgnyzfatmtpumgmuzymtnymgmuzfmtatayagmgnfmuntpuagatmgmgnuatzgagayatmtzgaumtnumgnumuntmfmgpfmgntmfpgntmgzgmtnyzymgmgpuatpuayzumgzgnumgagaymtzgmtaymuauzgauagmtnymgatmuzfpuzyayauagatzgztmgzgngmgaynuztmuatataypgpumgmtmuzgngnyaymgpfmgmgpuatmgnfnymgntmgnymgntmgauzgmtzfntmgntmgnuayauagatzfatmuzyaymtatmtaynumgpumgatatpgmgzgzfmtmfzgauagztmunfmgnt
добавить в отчет как кол-во текста влияет на качество частотного анализа

inanefforttoencourageecologicallysustainableforestrypracticesaninternationalorganizationstartedissuingcertificationstowoodcompaniesthatmeethighecologicalstandardsbyconservingresourcesandrecyclingmaterialscompaniesthatreceivethiscertificationcanattractcustomersbyadvertisingtheirproductsasecocertifiedaroundtheworldmanywoodcompanieshaveadoptednewecologicallyfriendlypracticesinordertoreceiveecocertificationhoweveritisunlikelythatwoodcompaniesintheunitedstateswilldothesameforseveralreasonsfirstamericanconsumersareexposedtosomuchadvertisingthattheywouldnotvalueorevenpayattentiontotheecocertificationlabelbecausesomanymediocreproductsarelabeledneworimprovedamericanconsumersdonotplacemuchtrustinadvertisingclaimsingeneralsecondecocertifiedwoodwillbemoreexpensivethanuncertifiedwoodbecauseinordertoearnecocertificationawoodcompanymustpaytohaveitsbusinessexaminedbyacertificationagencythisadditionalcostgetspassedontoconsumersamericanconsumerstendtobestronglymotivatedbypriceandthereforetheyarelikelytochoosecheaperuncertifiedwoodproductsaccordinglyamericanwoodcompanieswillprefertokeeptheirpriceslowratherthanobtainecocertificationthirdalthoughsomepeopleclaimthatitalwaysmakesgoodbusinesssenseforamericancompaniestokeepupwiththedevelopmentsintherestoftheworldthisargumentisnotconvincingpursuingcertificationwouldmakesenseforamericanwoodcompaniesonlyiftheymarketedmostoftheirproductsabroadbutthatisnotthecaseamericanwoodbusinessessellmostoftheirproductsintheunitedstatescateringtoaverylargecustomerbasethatissatisfiedwiththemerchandise

* z p n a m
g a b c d e
y f g h i j
u k l m n o
t p q r s t
f u v w x y
q z * * * *
"""
