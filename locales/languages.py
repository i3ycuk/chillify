# Количество языков на одной странице
LANGUAGES_PER_PAGE = 5

# Список кодов языков
LANGUAGES = [
    "ar", "az", "be", "bs", "ca", "cs", "da", "de", "el", "en", "es", "fi", 
    "fr", "ga", "he", "hi", "hr", "hu", "id", "it", "ja", "ka", "kk", "ko", "lt", "lv", 
    "mk", "ml", "mr", "ms", "nb", "ne", "pl", "pt", "ro", "ru", "sr", "sv", 
    "tr", "uk", "ur", "vi", "zh"
]

# Переводы языков на английский, русский и азербайджанский
LANGUAGES_TRANSLATIONS = {
    "ar": {"ar": "العربية", "az": "الأذربيجانية", "de": "الألمانية", "en": "الإنجليزية", "es": "الإسبانية", "fr": "الفرنسية", "he": "العبرية", "ja": "اليابانية", "ka": "الجورجية", "kk": "الكازاخية", "ko": "الكورية", "ru": "الروسية", "tr": "التركية", "uk": "الأوكرانية", "zh": "الصينية"},
    "az": {"ar": "Ərəb", "az": "Azərbaycan", "de": "Alman", "en": "İngilis", "es": "İspan", "fr": "Fransız", "he": "İvrit", "ja": "Yapon", "ka": "Gürcü", "kk": "Qazax", "ko": "Koreya", "ru": "Rus", "tr": "Türk", "uk": "Ukrayna", "zh": "Çin"},
    "de": {"ar": "Arabisch", "az": "Aserbaidschanisch", "de": "Deutsch", "en": "Englisch", "es": "Spanisch", "fr": "Französisch", "he": "Hebräisch", "ja": "Japanisch", "ka": "Georgisch", "kk": "Kasachisch", "ko": "Koreanisch", "ru": "Russisch", "tr": "Türkisch", "uk": "Ukrainisch", "zh": "Chinesisch"},
    "en": {"ar": "Arabic", "az": "Azerbaijani", "de": "German", "en": "English", "es": "Spanish", "fr": "French", "he": "Hebrew", "ja": "Japanese", "ka": "Georgian", "kk": "Kazakh", "ko": "Korean", "ru": "Russian", "tr": "Turkish", "uk": "Ukrainian", "zh": "Chinese"},
    "es": {"ar": "Árabe", "az": "Azerbaiyano", "de": "Alemán", "en": "Inglés", "es": "Español", "fr": "Francés", "he": "Hebreo", "ja": "Japonés", "ka": "Georgiano", "kk": "Kazajo", "ko": "Coreano", "ru": "Ruso", "tr": "Turco", "uk": "Ucraniano", "zh": "Chino"},
    "fr": {"ar": "Arabe", "az": "Azerbaïdjanais", "de": "Allemand", "en": "Anglais", "es": "Espagnol", "fr": "Français", "he": "Hébreu", "ja": "Japonais", "ka": "Géorgien", "kk": "Kazakh", "ko": "Coréen", "ru": "Russe", "tr": "Turc", "uk": "Ukrainien", "zh": "Chinois"},
    "he": {"ar": "ערבי", "az": "אזרית", "de": "גרמני", "en": "אנגלית", "es": "ספרדית", "fr": "צרפתי", "he": "עברית", "ja": "יפנית", "ka": "גאורגי", "kk": "קזחית", "ko": "קוריאנית", "ru": "רוסית", "tr": "טורקית", "uk": "אוקראינית", "zh": "סינית"},
    "ja": {"ar": "アラビア語", "az": "アゼルバイジャン語", "de": "ドイツ語", "en": "英語", "es": "スペイン語", "fr": "フランス語", "he": "ヘブライ語", "ja": "日本語", "ka": "ジョージア語", "kk": "カザフ語", "ko": "韓国語", "ru": "ロシア語", "tr": "トルコ語", "uk": "ウクライナ語", "zh": "中国語"},
    "ka": {"ar": "არაბული", "az": "აზერბაიჯანული", "de": "გერმანული", "en": "ინგლისური", "es": "ესპანური", "fr": "ფრანგული", "he": "ებრაული", "ja": "იაპონური", "ka": "ქართული", "kk": "ქაზახური", "ko": "კორეული", "ru": "რუსული", "tr": "თურქული", "uk": "უკრაინული", "zh": "ჩინური"},
    "kk": {"ar": "Араб тілі", "az": "Azərbaycan dili", "de": "Неміс тілі", "en": "Ағылшын тілі", "es": "Испан тілі", "fr": "Француз тілі", "he": "Иврит тілі", "ja": "Жапон тілі", "ka": "Грузин тілі", "kk": "Қазақ тілі", "ko": "Корей тілі", "ru": "Орыс тілі", "tr": "Түрік тілі", "uk": "Украин тілі", "zh": "Қытай тілі"},
    "ko": {"ar": "아랍어", "az": "아제르바이잔어", "de": "독일어", "en": "영어", "es": "스페인어", "fr": "프랑스어", "he": "히브리어", "ja": "일본어", "ka": "조지아어", "kk": "카자흐어", "ko": "한국어", "ru": "러시아어", "tr": "터키어", "uk": "우크라이나어", "zh": "중국어"},
    "ru": {"ar": "Арабский", "az": "Азербайджанский", "de": "Немецкий", "en": "Английский", "es": "Испанский", "fr": "Французский", "he": "Иврит", "ja": "Японский", "ka": "Грузинский", "kk": "Казахский", "ko": "Корейский", "ru": "Русский", "tr": "Турецкий", "uk": "Украинский", "zh": "Китайский"},
    "tr": {"ar": "Arapça", "az": "Azerice", "de": "Almanca", "en": "İngilizce", "es": "İspanyolca", "fr": "Fransızca", "he": "İbranice", "ja": "Japonca", "ka": "Gürcüce", "kk": "Kazakça", "ko": "Korece", "ru": "Rusça", "tr": "Türkçe", "uk": "Ukraynaca", "zh": "Çince"},
    "uk": {"ar": "Арабська", "az": "Азербайджанська", "de": "Німецька", "en": "Англійська", "es": "Іспанська", "fr": "Французька", "he": "Іврит", "ja": "Японська", "ka": "Грузинська", "kk": "Казахська", "ko": "Корейська", "ru": "Російська", "tr": "Турецька", "uk": "Українська", "zh": "Китайська"},
    "zh": {"ar": "阿拉伯语", "az": "阿塞拜疆语", "de": "德语", "en": "英语", "es": "西班牙语", "fr": "法语", "he": "希伯来语", "ja": "日语", "ka": "格鲁吉亚语", "kk": "哈萨克语", "ko": "韩语", "ru": "俄语", "tr": "土耳其语", "uk": "乌克兰语", "zh": "中文"}
}

LANGUAGES_FLAGS = {
    "ar": "🇸🇦", "az": "🇦🇿", "be": "🇧🇾", "bs": "🇧🇦", "ca": "🇪🇸", "cs": "🇨🇿",
    "da": "🇩🇰", "de": "🇩🇪", "el": "🇬🇷", "en": "🇺🇸", "es": "🇪🇸", "fi": "🇫🇮",
    "fr": "🇫🇷", "ga": "🇮🇪", "he": "🇮🇱", "hi": "🇮🇳", "hr": "🇭🇷", "hu": "🇭🇺",
    "id": "🇮🇩", "it": "🇮🇹", "ja": "🇯🇵", "ka": "🇬🇪", "kk": "🇰🇿", "ko": "🇰🇷", "lt": "🇱🇹", "lv": "🇱🇻",
    "mk": "🇲🇰", "ml": "🇮🇳", "mr": "🇮🇳", "ms": "🇲🇾", "nb": "🇳🇴", "ne": "🇳🇵",
    "pl": "🇵🇱", "pt": "🇵🇹", "ro": "🇷🇴", "ru": "🇷🇺", "sr": "🇷🇸", "sv": "🇸🇪",
    "tr": "🇹🇷", "uk": "🇺🇦", "ur": "🇵🇰", "vi": "🇻🇳", "zh": "🇨🇳"
}