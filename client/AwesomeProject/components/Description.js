import { StyleSheet, Text, View, Picker, Button } from 'react-native';
import { useEffect, useState } from 'react';

const Description = (props) => {
    return (
        <View style={styles.container}>
            <Text>Name: {props.name}</Text>
            <Text>Hand: {props.hand}</Text>
            <Text>Height: {props.height}</Text>
            <Text>Country: {props.country}</Text>
            <Text>Age: {props.age}</Text>
            <Text>Rank: {props.rank}</Text>
            <Text>Wins: {props.wins}</Text>
            <Text>Losses: {props.losses}</Text>
            <Text>Number of Matches: {props.no_of_matches}</Text>
            <Text>Total Minutes Played: {props.total_minutes}</Text>
        </View>
    )
}

export default Description;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#d3d3d3',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 4,
        width: 300,
        height: 300
    },
});
