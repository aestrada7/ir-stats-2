"use client";
import { useState } from "react";

import Classes from "./SeasonTable.module.scss";
import SessionInfo from "@/components/SessionInfo/SessionInfo";

export default function SeasonTable(props) {
    let [ sessions, setSessions ] = useState(props.sessions);
    let [ sortField, setSortField ] = useState();
    let [ sortOrder, setSortOrder ] = useState();

    function sortBy(field, order) {
        let sortedSessions = [...sessions];
        sortedSessions.sort((x, y) => order == 'ASC' ? y[field] - x[field] : x[field] - y[field]);
        setSortField(field);
        setSortOrder(order);
        setSessions(sortedSessions);
    }

    function sortableField(field, sortField, sortOrder) {
        return (
            <div>
                <div className={`${Classes.sortDown} ${sortField === field && sortOrder === 'ASC' ? Classes.selected : ''}`} 
                     onClick={() => sortBy(field, 'ASC')}></div>
                <div className={`${Classes.sortUp} ${sortField === field && sortOrder === 'DESC' ? Classes.selected : ''}`} 
                     onClick={() => sortBy(field, 'DESC')}></div>
            </div>
        )
    }

    return (
        <div className={Classes.season}>
            <div className={Classes.seasonTitle}>Detailed Results</div>
            <div className={Classes.seasonHeader}>
                <div className={Classes.largeHeader}>Race Info</div>
                <div className={Classes.simpleHeader}>
                    <p>SOF</p>
                    { sortableField('sof', sortField, sortOrder) }
                </div>
                <div className={Classes.simpleHeader}>
                    <p>Points</p>
                    { sortableField('champ_points', sortField, sortOrder) }
                </div>
                <div className={Classes.simpleHeader}>Laps/Total</div>
                <div className={Classes.simpleHeader}>
                    <p>Led</p>
                    { sortableField('led', sortField, sortOrder) }
                </div>
                <div className={Classes.simpleHeader}>
                    <p>Start</p>
                    { sortableField('starting_position', sortField, sortOrder) }
                </div>
                <div className={Classes.simpleHeader}>
                    <p>Finish</p>
                    { sortableField('finishing_position', sortField, sortOrder) }
                </div>
            </div>
            { sessions.map((session) => (
                <SessionInfo key={`${session.session_id}`} session={session}></SessionInfo>
            ))}
        </div>
    )
}