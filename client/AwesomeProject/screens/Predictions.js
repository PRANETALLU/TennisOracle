import { StyleSheet, Text, View, Button, ActivityIndicator } from 'react-native';
import { useEffect, useState, useRef } from 'react';
import { useNavigation } from "@react-navigation/native";
import { Picker } from '@react-native-picker/picker';
import Icon from 'react-native-vector-icons/FontAwesome';


const Predictions = () => {
    const [playerNames, setPlayerNames] = useState([])
    const [name1, setName1] = useState("")
    const [name2, setName2] = useState("")
    const [winner, setWinner] = useState()
    const navigation = useNavigation()
    const scrollViewRef = useRef(null)
    const [predictClicked, setPredictClicked] = useState(false);
    const [loading, setLoading] = useState(false)

    const setName1Function = (item) => {
        setName1(item)
        setPredictClicked(false)
        setLoading(false)
    }

    const setName2Function = (item) => {
        setName2(item)
        setPredictClicked(false)
        setLoading(false)
    }

    const getPlayerInfo = async () => {
        const response = await fetch('http://127.0.0.1:8000/getPlayerInfo', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        const data = await response.json();
        setPlayerNames(data.players)
    }

    const getWinner = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:8000/predictWinner', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    p1_name: name1,
                    p2_name: name2
                })
            });

            if (!response.ok) {
                throw new Error('Failed to predict winner');
            }

            const data = await response.json();
            setWinner(data.Winner);
            //scrollViewRef.current.scrollToEnd({ animated: true });
        } catch (error) {
            console.error('Error predicting winner:', error);
            // Handle error here, e.g., setWinner(null) or show an error message
        } finally {
            setLoading(false);
            setPredictClicked(true);
        }
    }

    useEffect(() => {
        getPlayerInfo()
    }, [])


    return (
        <View style={{ flex: 1, backgroundColor: '#fff' }}>
            <View style={{ alignItems: "flex-end", paddingTop: 5, paddingRight: 5 }}>
                <Button title="Database Search" onPress={() => navigation.navigate("DatabaseSearch")} />
            </View>
            <View style={{
                flexDirection: "column", alignItems: "center", paddingTop: "10%", rowGap: 5
            }}>
                <View style={{ display: "flex", flexDirection: "row", columnGap: 5 }}>
                    <Picker selectedValue={name1} onValueChange={(itemValue, itemIndex) => setName1Function(itemValue)}>
                        {["Select Player 1", ...playerNames].map((playerName) => (
                            <Picker.Item label={playerName.name} value={playerName.name} />
                        ))}
                    </Picker>
                    <Picker selectedValue={name2} onValueChange={(itemValue, itemIndex) => setName2Function(itemValue)}>
                        {["Select Player 2", ...playerNames].map((playerName) => (
                            <Picker.Item label={playerName.name} value={playerName.name} />
                        ))}
                    </Picker>
                </View>
                <Button title="Predict" onPress={getWinner} />
                {loading ? ( // Display ActivityIndicator while loading
                    <ActivityIndicator size="large" color="#0000ff" />
                ) : predictClicked && winner !== undefined ? ( // Display winner only if prediction is made and winner is defined
                    <Text>Winner: {winner == 1 ? name1 : name2}</Text>
                ) : null} 
            </View>
        </View>
    )
}

export default Predictions;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
});
