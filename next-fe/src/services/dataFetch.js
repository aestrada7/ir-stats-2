import { PYRA_BASE_URL } from "./config";

/**
 * Retrieves all existing seasons stored in the database.
 * 
 * @param {number} custid The customer id to filter by.
 * @param {number} seriesid The series id to filter by.
 * @returns {object} The JSON object with all recorded seasons for the filtered combination.
 */
export const getSeasonList = async(cust_id, series_id) => {
    const url = await fetch(`${PYRA_BASE_URL}/api/seasons?cust_id=${cust_id}`);
    console.log(`hi ${PYRA_BASE_URL}`);
    return await url.json();
}