/**
 * Converts a stored time to a date/time readable string.
 * 
 * @param {string} date An iracing stored date/time combination.
 * @returns {string} A readable formatted string
 */
export const formatDateTime = (date) => {
    if(date) {
        let d = new Date(date);
        return d.toLocaleString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', year: 'numeric', month: 'numeric', day: 'numeric' });
    } 
}