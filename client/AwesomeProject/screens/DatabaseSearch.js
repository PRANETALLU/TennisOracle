import { StyleSheet, Text, View, Button, ScrollView, Alert, Dimensions, TextInput } from 'react-native';
import { useEffect, useState } from 'react';
import Description from '../components/Description.js';
import { Picker } from '@react-native-picker/picker';
import AsyncStorage from '@react-native-async-storage/async-storage';

const DatabaseSearch = () => {
    const [playerInfo, setPlayerInfo] = useState([])

    const [nameChoice, setNameChoice] = useState("")
    const [handChoice, setHandChoice] = useState("")
    const [countryChoice, setCountryChoice] = useState("")
    const [minAge, setMinAge] = useState("");
    const [maxAge, setMaxAge] = useState("");
    const [rankRange, setRankRange] = useState("");
    const [minHeight, setMinHeight] = useState("");
    const [maxHeight, setMaxHeight] = useState("");
    const [numMatch, setNumMatch] = useState(""); 

    const [playerNameArray, setPlayerNameArray] = useState([])
    const [playerHandArray, setPlayerHandArray] = useState([])
    const [playerCountryArray, setPlayerCountryArray] = useState([])

    const [description, setDescription] = useState([])

    const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

    const getPlayerInfo = async () => {
        const response = await fetch('http://127.0.0.1:8000/getPlayerInfo', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        const data = await response.json();
        setPlayerInfo(data.players)
    }


    useEffect(() => {
        getPlayerInfo()
    }, [])

    const resetParameters = () => {
        const nameSet = new Set()
        const handSet = new Set()
        const countrySet = new Set()
        playerInfo.map((pInfo) => {
            nameSet.add(pInfo.name)
            handSet.add(pInfo.hand)
            countrySet.add(pInfo.country)
        })

        const nameArray = Array.from(nameSet)
        nameArray.sort()
        setPlayerNameArray(nameArray)

        const hArray = Array.from(handSet)
        hArray.sort()
        setPlayerHandArray(hArray)

        const coArray = Array.from(countrySet)
        coArray.sort()
        setPlayerCountryArray(coArray)
    }

    useEffect(() => {
        resetParameters()
    }, [playerInfo])

    const getDescriptions = async () => {
        if (handChoice == "Select Hand" && countryChoice == "Select Country") {
            Alert.alert("Please select all choices")
            return;
        }
        const response = await fetch('http://127.0.0.1:8000/searchFilter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: nameChoice,
                hand: handChoice,
                country: countryChoice,
                minAge: minAge,
                maxAge: maxAge,
                rankRange: rankRange,
                minHeight: minHeight,
                maxHeight: maxHeight
            })
        })
        const data = await response.json();
        setDescription(data.players)
    }

    console.log("Name Choice: " + nameChoice)
    console.log("Hand Choice: " + handChoice)
    console.log("Country Choice: " + countryChoice)
    console.log("Min Age: " + minAge)

    return (
        <ScrollView contentContainerStyle={styles.scrollViewContainer}>
            <View style={{ flex: 1, backgroundColor: '#fff' }}>
                <View style={{ display: "flex", flexDirection: "row" }}>
                    <View style={{
                        flexDirection: "column",
                        width: screenWidth * 0.3,
                        minHeight: screenHeight,
                        borderWidth: 1,
                        borderColor: 'black',
                        borderStyle: 'solid',
                        rowGap: 20,
                        paddingLeft: 5,
                        paddingRight: 5,
                        justifyContent: 'center'
                    }}>
                        <Picker selectedValue={nameChoice} onValueChange={(itemValue, itemIndex) => setNameChoice(itemValue)}>
                            {["Select Player Name", ...playerNameArray].map((name) => (
                                <Picker.Item label={name} value={name} />
                            ))}
                        </Picker>
                        <Picker selectedValue={handChoice} onValueChange={(itemValue, itemIndex) => setHandChoice(itemValue)}>
                            {["Select Hand", ...playerHandArray].map((hand) => (
                                <Picker.Item label={hand} value={hand} />
                            ))}
                        </Picker>
                        <Picker selectedValue={countryChoice} onValueChange={(itemValue, itemIndex) => setCountryChoice(itemValue)}>
                            {["Select Country", ...playerCountryArray].map((country) => (
                                <Picker.Item label={country} value={country} />
                            ))}
                        </Picker>
                        <TextInput style={styles.button} placeholder='Min Age' value={minAge} onChangeText={(minAge) => setMinAge(minAge)} />
                        <TextInput style={styles.button} placeholder='Max Age' value={maxAge} onChangeText={(maxAge) => setMaxAge(maxAge)} />
                        <TextInput style={styles.button} placeholder='Min Height (cm)' value={minHeight} onChangeText={(minHeight) => setMinHeight(minHeight)} />
                        <TextInput style={styles.button} placeholder='Max Height (cm)' value={maxHeight} onChangeText={(maxHeight) => setMaxHeight(maxHeight)} />
                        <Picker selectedValue={rankRange} onValueChange={(itemValue, itemIndex) => setRankRange(itemValue)}>
                            {["Select Rank", "0 - 100", "101 - 500", "501 - 1000"].map((rankR) => (
                                <Picker.Item label={rankR} value={rankR} />
                            ))}
                        </Picker>
                        <Picker selectedValue={numMatch} onValueChange={(itemValue, itemIndex) => setNumMatch(itemValue)}>
                            {["Select Number of Matches", "0 - 100", "101 - 200", "201 - 300", "301 - 400"].map((numM) => (
                                <Picker.Item label={numM} value={numM} />
                            ))}
                        </Picker>
                        <Button title='Search' onPress={getDescriptions} />
                    </View>
                    <ScrollView contentContainerStyle={styles.scrollViewContainer}>
                        <View style={{
                            flex: 1,
                            flexDirection: "column",
                            width: screenWidth * 0.7,
                            height: "100%",
                            borderWidth: 1,
                            borderColor: 'black',
                            borderStyle: 'solid',
                            alignItems: "center",
                            paddingTop: 5
                        }}>
                            {description.length > 0 ? description.map((des) => (
                                <Description
                                    name={des.name}
                                    hand={des.hand}
                                    height={des.height}
                                    country={des.country}
                                    age={des.age}
                                    rank={des.rank}
                                    wins={des.num_of_wins}
                                    losses={des.num_of_loss}
                                    no_of_matches={des.no_of_matches}
                                    total_minutes={des.total_minutes}
                                />
                            )) : <Text>No results</Text>}
                        </View>
                    </ScrollView>
                </View>
            </View>
        </ScrollView>
    )
}

export default DatabaseSearch;

const styles = StyleSheet.create({
    scrollViewContainer: {
      
    },
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    column: {
        flexDirection: 'column',
    },
    button: {
        borderColor: 'black', 
        borderWidth: 1, 
    }
});