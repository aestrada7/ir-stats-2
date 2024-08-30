/**
 * Builds the stats box data or adding results.
 * 
 * @param {object} data The raw data with all races for a given period of time.
 * @returns {object} An object with the bvox stats data.
 */
export const statsBoxDataBuild = (data) => {
    let newData = {};
    newData.races = data.length;
    newData.wins = data.filter(x => x.finishing_position == 1).length;
    newData.top5s = data.filter(x => x.finishing_position <= 5).length;
    newData.top10s = data.filter(x => x.finishing_position <= 10).length;
    newData.totalLaps = data.reduce((acc, val) => { return acc + val.event_laps_complete}, 0);
    newData.actualLaps = data.reduce((acc, val) => { return acc + val.laps}, 0);
    newData.lapsLed = data.reduce((acc, val) => { return acc + val.led}, 0);
    newData.poles = data.filter(x => x.starting_position == 1).length;
    newData.dnfs = data.filter(x => x.dnf).length;
    newData.avgStart = (data.reduce((acc, val) => { return acc + val.starting_position}, 0) / newData.races).toPrecision(3);
    newData.avgFinish = (data.reduce((acc, val) => { return acc + val.finishing_position }, 0) / newData.races).toPrecision(3);
    newData.avgFinishSansDnfs = (data.reduce((acc, val) => { return acc + (!val.dnf ? val.finishing_position : 0) }, 0) / (newData.races - newData.dnfs)).toPrecision(3);
    newData.bestResult = Math.min.apply(Math, data.map(x => x.finishing_position));

    newData.top5Percentage = ((newData.top5s / newData.races) * 100).toPrecision(3);
    newData.top10Percentage = ((newData.top10s / newData.races) * 100).toPrecision(3);
    newData.actualLapsPercentage = ((newData.actualLaps / newData.totalLaps) * 100).toPrecision(3);
    newData.ledPercentage = ((newData.lapsLed / newData.totalLaps) * 100).toPrecision(3);
    newData.winPercentage = ((newData.wins / newData.races) * 100).toPrecision(3);
    newData.dnfPercentage = ((newData.dnfs / newData.races) * 100).toPrecision(3);

    if(isNaN(newData.avgFinishSansDnfs)) {
        newData.avgFinishSansDnfs = 0;
    }

    return newData;
}
