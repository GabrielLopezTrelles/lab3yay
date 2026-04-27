import streamlit as st
import google.generativeai as genai
import requests
baseUrl = "http://ws.audioscrobbler.com/2.0"
apiKey = "a28edaddcd62a1f9f8ae8100299fbc3b"
st.set_page_config(page_title="Music Chatbot", page_icon="", layout="wide")

key = st.secrets["key"]

genai.configure(api_key = key)

st.title("Travel Music")
st.markdown("This is your one-stop shop for understanding the music taste in the countries you're traveling to!")
st.image("WebDevelopmentLab03/images/lemondemon.jpg", width=300)

with st.form("survey_form"):
    country = st.selectbox("What country are you visiting?", [
        "AFGHANISTAN", "ALBANIA", "ALGERIA", "AMERICAN SAMOA", "ANDORRA","ANGOLA","ANGUILLA","ARGENTINA","ARMENIA",	"ARUBA","AUSTRALIA","AUSTRIA","AZERBAIJAN","BAHAMAS","BAHRAIN","BANGLADESH","BARBADOS","BELARUS","BELGIUM","BELIZE","BENIN","BERMUDA","BHUTAN",	"BOLIVIA, PLURINATIONAL STATE OF","BOSNIA AND HERZEGOVINA","BOTSWANA","BRAZIL","BRUNEI DARUSSALAM",	"BULGARIA","BURKINA FASO","BURUNDI","CAMBODIA","CAMEROON","CANADA","CABO VERDE","CENTRAL AFRICAN REPUBLIC","CHAD","CHILE","CHINA","COLOMBIA","COMOROS","CONGO","CONGO, THE DEMOCRATIC REPUBLIC OF THE","COOK ISLANDS","COSTA RICA","CROATIA","CUBA","CYPRUS","CZECHIA","DENMARK","DJIBOUTI","DOMINICA","DOMINICAN REPUBLIC","ECUADOR","EGYPT","EL SALVADOR","EQUATORIAL GUINEA","ERITREA","ESTONIA","ETHIOPIA","FAROE ISLANDS","FIJI","FINLAND","FRANCE","GABON","GAMBIA","GEORGIA","GERMANY","GHANA","GIBRALTAR","GREECE","GREENLAND","GRENADA","GUAM","GUATEMALA","GUINEA","GUINEA-BISSAU","GUYANA","HAITI","HONDURAS","HONG KONG","HUNGARY","ICELAND","INDIA","INDONESIA","IRAN, ISLAMIC REPUBLIC OF","IRAQ","IRELAND","ISRAEL","ITALY","JAMAICA","JAPAN","JORDAN","KAZAKHSTAN","KENYA","KIRIBATI","KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF","KOREA, REPUBLIC OF","KUWAIT","KYRGYZSTAN","LAO PEOPLE'S DEMOCRATIC REPUBLIC","LATVIA","LEBANON","LESOTHO","LIBERIA","LIBYA","LIECHTENSTEIN","LITHUANIA","LUXEMBOURG","MADAGASCAR","MALAWI","MALAYSIA","MALDIVES","MALI","MALTA","MARSHALL ISLANDS","MAURITANIA","MAURITIUS","MEXICO","MICRONESIA, FEDERATED STATES OF","MONACO","MONGOLIA","MONTENEGRO","MOROCCO","MOZAMBIQUE","MYANMAR","NAMIBIA","NAURU","NEPAL","NETHERLANDS","NEW ZEALAND","NICARAGUA","NIGER","NIGERIA","NORWAY","OMAN","PAKISTAN","PALAU","PALESTINE, STATE OF","PANAMA","PAPUA NEW GUINEA","PARAGUAY","PERU","PHILIPPINES","POLAND","PORTUGAL","PUERTO RICO","QATAR","ROMANIA","RUSSIAN FEDERATION","RWANDA","SAINT KITTS AND NEVIS","SAINT LUCIA","SAINT VINCENT AND THE GRENADINES","SAMOA","SAN MARINO","SAO TOME AND PRINCIPE","SAUDI ARABIA","SENEGAL","SERBIA","SEYCHELLES","SIERRA LEONE","SINGAPORE","SLOVAKIA","SLOVENIA","SOLOMON ISLANDS","SOMALIA","SOUTH AFRICA","SPAIN","SRI LANKA","SUDAN","SURINAME","SWAZILAND","SWEDEN","SWITZERLAND","SYRIAN ARAB REPUBLIC","TAJIKISTAN","TANZANIA, UNITED REPUBLIC OF","THAILAND","TIMOR-LESTE","TOGO","TONGA","TRINIDAD AND TOBAGO","TUNISIA","TURKEY","TURKMENISTAN","TUVALU","UGANDA","UKRAINE","UNITED ARAB EMIRATES","UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND","UNITED STATES OF AMERICA","URUGUAY","UZBEKISTAN","VANUATU","VENEZUELA, BOLIVARIAN REPUBLIC OF","VIET NAM","WESTERN SAHARA","YEMEN","ZAMBIA","ZIMBABWE"
    ], index=None)
    genre = st.selectbox("What genre of music do you enjoy?", [
        "rock","electronic","pop","indie","metal","alternative rock","jazz","classic rock","ambient","experimental","folk","indie rock","punk","Hip-Hop","hard rock","black metal","instrumental","dance","80s","death metal","Progressive rock",
        "heavy metal","hardcore","british","soul","chillout","electronica","rap","industrial","punk rock","Classical","Soundtrack",
        "blues","thrash metal","90s","metalcore","psychedelic","acoustic","hip hop","post-rock","Progressive metal","House","german","techno",
        "new wave","trance","funk","post-punk","piano","indie pop","reggae","70s","electro","trip-hop","rnb","60s","country","Power metal",
        "Melodic Death Metal","downtempo","emo","post-hardcore","doom metal","Psychedelic Rock","synthpop","oldies","Love","00s","Gothic Metal",
        "cover","noise","dark ambient","idm","Grunge","guitar","jazz fusion","Gothic","pop rock","britpop","screamo","swedish","favorites","lounge",
        "Mellow","Nu Metal","grindcore","j-pop"
    ], index=None)

    def topArtists(country, genre):
        try:
            baseUrl = 'http://ws.audioscrobbler.com/2.0'
            apiKey = "a28edaddcd62a1f9f8ae8100299fbc3b"
            urlCountry = country.replace(" ", "+")
            addBaseCountryurl = baseUrl + "/?method=geo.gettopartists=" + urlCountry
            endpoint1 = addBaseCountryurl + "&api_key=" + apiKey + "&format=json"
            response1 = requests.get(endpoint1)
            data1 = response1.json()
            countryGetArtist = []
            for a in data1["topartists"]["artist"]:
                countryGetArtist.append(a["name"])
            urlGenre = genre.replace(" ", "+")
            addBaseGenreurl = baseUrl + "/?method=tag.gettopartists=" + urlGenre
            endpoint2 = addBaseGenreurl + "&api_key=" + apiKey + "&format=json"
            response2 = requests.get(endpoint2)
            data2 = response2.json()
            getArtist = []
            for b in data2["topartists"]["artist"]:
                if b["name"] in countryGetArtist:
                    response3 = requests.get(f"{baseUrl}/?method=artist.getinfo&artist={b["name"].replace(" ", "+")}&api_key={apiKey}&format=json")
                    data3 = response3.json()
                    getArtist.append(f"{b["name"]}  - {b["url"]}, {data3["artist"]["bio"]["summary"]}")
            return getArtist
        except:
            return "Sorry, the country you entered likely doesn't have listeners right now."
    submitted = st.form_submit_button("Submit Data")

    if submitted:
        try:
            response = genai.GenerativeModel.generate_content(model="gemini-3-flash-preview",
        contents=f"Write a guide to listening to music in the genre {genre} while on vacation in the country {country}. If possible, recommend these top artists to listen to and why based on this API data: {topArtists(country, genre)}")
            st.write(response.text)

        except Exception as e:
            error_message = str(e).lower()

            if "quota" in error_message or "rate" in error_message or "429" in error_message:
                assistant_reply = f"FULL ERROR: {e}"
            elif "safety" in error_message or "blocked" in error_message:
                assistant_reply = "Error. I can't respond to that topic. Try asking me something else about music!"
            else:
                assistant_reply = f"Error. Something went wrong. Please try again. (Error: {str(e)})"

            with st.chat_message("assistant"):
                st.markdown(assistant_reply)
