import streamlit as st
import requests
#Goal: box that you input artist and you get similar artists and input song and you get similar songs

st.title("DJ Helper")
st.write("Welcome to DJ Helper! Enter a song and we will return a list of similar songs and similar artists to jumpstart your mixes! Customize artists and song popularity. We will do the rest!")


#Base URL and API Key

baseUrl = 'http://ws.audioscrobbler.com/2.0'
apiKey = "a28edaddcd62a1f9f8ae8100299fbc3b"


with st.form("song_search"):
    theSong = st.text_input("Search: What song do you want to mix?", value=None)
    theArtist = st.text_input("Input the artist! (optional, must be accurate)", value=None)
    submitted = st.form_submit_button("Submit Data")
    if submitted:
        def confirmSong(theArtist, theSong):
            addBaseArtisturl = baseUrl + "method=track.search"
            trackk = theSong.replace(" ", "+")
            artistt = theArtist.replace(" ", "+")
            if artistt != None:
                endpoint3 = addBaseArtisturl + "&track=" + trackk + "&artist=" + artistt + "&api_key=" + apiKey + "&format=json"
            else:
                endpoint3 = addBaseArtisturl + "&track=" + trackk + "&api_key=" + apiKey + "&format=json"
            response3 = requests.get(endpoint3)
            data = response3.json()
            confirmSongList = []
            try:
                for d in data["trackmatches"]["track"]:
                    if len(confirmSongList) < 5:
                        confirmSongList.append(f"{d["name"]} by {d["artist"]}")
                    else:
                        break
                
                for num in range(len(confirmSongList)):
                    if st.button(confirmSongList[num], type="tertiary"):
                        st.write(f"You chose {confirmSongList[num]}!")
                        framework = data["trackmatches"]["track"][num]
                    else:
                        st.write("Choose a song!")
                        framework = None
                return framework
            except:
                "An error occured. Try entering a new song or artist name."

with st.form("survey_form"):
    boolExpressionPlays = st.checkbox("Only the hits")
    boolExpressionArtist = st.checkbox("Show songs from other artists")

    ###Confirm Song Function:


    inputArtist = framework["artist"]
    inputSong = framework["name"]

    ###Similar Artists Function:

    def getSimilarArtists(inputArtist):

        #Endpoint code:

        addBaseArtisturl = baseUrl + "/?method=artist.getsimilar&artist="
        urlArtist = inputArtist.replace(" ", "+")
        endpoint1 = addBaseArtisturl + urlArtist + "&api_key=" + apiKey + "&format=json"
        response1 = requests.get(endpoint1)

        #Return the list code:

        try:
            data1 = response1.json()
            similarArtistList = []
            for i in data1["similarartists"]["artist"]:
                if float(i["match"]) <= 1 and float(i["match"]) >= .5:
                    similarArtistList.append(i["name"])
            return similarArtistList
        
        except:
            return "Bad response. Try capitalizing the artist name."

    ###Similar Artists Function:

    def getSimilarArtists(inputArtist):

        #Endpoint code:

        addBaseArtisturl = baseUrl + "/?method=artist.getsimilar&artist="
        urlArtist = inputArtist.replace(" ", "+")
        endpoint1 = addBaseArtisturl + urlArtist + "&api_key=" + apiKey + "&format=json"
        response1 = requests.get(endpoint1)

        #Return the list code:

        try:
            data1 = response1.json()
            similarArtistList = []
            for i in data1["similarartists"]["artist"]:
                if float(i["match"]) <= 1 and float(i["match"]) >= .5:
                    similarArtistList.append(i["name"])
            return similarArtistList
        
        except:
            return "Bad response. Try capitalizing the artist name."

    ###Similar Songs Function:

    def getSimilarSongs(inputSong, inputArtist):

        #Endpoint code:
        
        urlArtist = inputArtist.replace(" ", "+")
        addBaseSongurl = baseUrl + "/?method=track.getsimilar&artist=" + urlArtist
        urlSong = inputSong.replace(" ", "+")
        endpoint2 = addBaseSongurl + "&track=" + urlSong + "&api_key=" + apiKey + "&format=json"
        response2 = requests.get(endpoint2)

        #Return the list code:
        data2 = response2.json()
        similarSongList = []
        for i in data2["similartracks"]["track"]:
            if float(i["match"]) <= 1 and float(i["match"]) >= .5:
                if boolExpressionArtist and not boolExpressionPlays:
                    if i["artist"]["name"].lower() != inputArtist.lower():
                        similarSongList.append(i["name"])
                elif not boolExpressionArtist and boolExpressionPlays:
                    if int(i["playcount"]) >= 100000:
                        similarSongList.append(i["name"])
                elif boolExpressionArtist and boolExpressionPlays:
                    if i["artist"]["name"].lower() != inputArtist.lower():
                        if int(i["playcount"]) >= 100000:
                            similarSongList.append(i["name"])
            else:
                similarSongList.append(i["name"])         
        return similarSongList
        
    submitted = st.form_submit_button("Submit Data")
    if submitted:
        st.write("**You may like these artists:**")
        for a in getSimilarArtists(inputArtist):
            st.write(f"{a}")
        st.write("\n**You may like these songs:**")
        for p in getSimilarSongs(inputSong, inputArtist):
            st.write(f"{p}")


