from django.utils import timezone
from .models import Profile

def set_timezone(get_response):
    
    def middleware(request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and request.user.profile.timezone:
                timezone.activate(request.user.profile.timezone)
            else:
                # If profile has no timeznoe we guess baed on LANG
                accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
                user_locale = accept_language.split(',')[0].split('-')[0]

                language_to_timezone = {
                    'en': 'America/New_York',      # English (United States)
                    'es': 'America/Mexico_City',   # Spanish (Mexico)
                    'fr': 'Europe/Paris',          # French (France)
                    'de': 'Europe/Berlin',         # German (Germany)
                    'ja': 'Asia/Tokyo',            # Japanese (Japan)
                    'zh': 'Asia/Shanghai',         # Chinese (China)
                    'ko': 'Asia/Seoul',            # Korean (South Korea)
                    'it': 'Europe/Rome',           # Italian (Italy)
                    'pt': 'America/Sao_Paulo',     # Portuguese (Brazil)
                    'ru': 'Europe/Moscow',         # Russian (Russia)
                    'ar': 'Asia/Riyadh',           # Arabic (Saudi Arabia)
                    'hi': 'Asia/Kolkata',          # Hindi (India)
                    'tr': 'Europe/Istanbul',       # Turkish (Turkey)
                    'nl': 'Europe/Amsterdam',      # Dutch (Netherlands)
                    'sv': 'Europe/Stockholm',      # Swedish (Sweden)
                    'pl': 'Europe/Warsaw',         # Polish (Poland)
                    'cs': 'Europe/Prague',         # Czech (Czech Republic)
                    'th': 'Asia/Bangkok',          # Thai (Thailand)
                    'el': 'Europe/Athens',         # Greek (Greece)
                    'hu': 'Europe/Budapest',       # Hungarian (Hungary)
                    'da': 'Europe/Copenhagen',     # Danish (Denmark)
                    'fi': 'Europe/Helsinki',       # Finnish (Finland)
                    'no': 'Europe/Oslo',           # Norwegian (Norway)
                    'he': 'Asia/Jerusalem',        # Hebrew (Israel)
                    'id': 'Asia/Jakarta',          # Indonesian (Indonesia)
                    'ro': 'Europe/Bucharest',      # Romanian (Romania)
                    'uk': 'Europe/Kiev',           # Ukrainian (Ukraine)
                    'bg': 'Europe/Sofia',          # Bulgarian (Bulgaria)
                    'hr': 'Europe/Zagreb',         # Croatian (Croatia)
                    'sr': 'Europe/Belgrade',       # Serbian (Serbia)
                    'sk': 'Europe/Bratislava',     # Slovak (Slovakia)
                    'sl': 'Europe/Ljubljana',      # Slovenian (Slovenia)
                    'et': 'Europe/Tallinn',        # Estonian (Estonia)
                    'lv': 'Europe/Riga',           # Latvian (Latvia)
                    'lt': 'Europe/Vilnius',        # Lithuanian (Lithuania)
                    'ms': 'Asia/Kuala_Lumpur',     # Malay (Malaysia)
                    'vi': 'Asia/Ho_Chi_Minh',      # Vietnamese (Vietnam)
                    'pt-BR': 'America/Sao_Paulo',  # Portuguese (Brazil)
                    'es-419': 'America/Mexico_City',# Spanish (Latin America)
                    'ca': 'Europe/Andorra',        # Catalan (Andorra)
                    'eu': 'Europe/Bilbao',         # Basque (Spain)
                    'gl': 'Europe/Madrid',         # Galician (Spain)
                    'af': 'Africa/Johannesburg',   # Afrikaans (South Africa)
                }
                default_timezone = 'UTC'
                user_timezone = language_to_timezone.get(user_locale, default_timezone)

                if hasattr(request.user, 'profile'):
                    request.user.profile.timezone = user_timezone
                else:
                    Profile(user=request.user, timezone=user_timezone).save()

                timezone.activate(user_timezone)
        else:
            timezone.deactivate()
        return get_response(request)

    return middleware
