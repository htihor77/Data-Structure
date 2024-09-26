import React, { useState } from 'react';

function DatabaseHealthCheckReports(props) {
  const [killedItems, setKilledItems] = useState({});

  const killProcess = async (item) => {
    console.log("Killing process for item:", item);
    let instId = item.INST_ID;
    let sid = item.SID;
    let serialNum = item.SERIAL;

    // Dummy environment check (replace with actual logic)
    let env = '';
    if (item.env === 'AWS-PROD' || env === 'ONPREM-PROD') {
      env = 'prod';
    } else {
      env = 'non-prod';
    }

    try {
      // Axios POST request to kill the session
      const response = await axiosConfig.post('/DatabaseHealthCheckReports/kill_session', {
        env,
        instId,
        sid,
        serialNum,
      });

      if (response.status === 200) {
        // Update the killedItems state for the specific SID
        setKilledItems((prevKilledItems) => ({
          ...prevKilledItems,
          [sid]: true,  // Mark this SID as killed
        }));

        // Show the alert with the SID
        alert(`Session for SID: ${sid} killed successfully`);

        // Optionally reset the message or any other functionality after killing
        setTimeout(() => {
          setKilledItems((prevKilledItems) => ({
            ...prevKilledItems,
            [sid]: false,  // Optionally reset the killed state after 3 seconds
          }));
        }, 3000);
      }
    } catch (error) {
      console.error('Error killing session:', error);
    }
  };

  const renderTable = (groupedData) => {
    return (
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
        <thead>
          <tr>
            {props.keys.map((key) => (
              <th key={key} style={{ border: '1px solid #ddd', padding: '8px' }}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {groupedData.map((group, rowIndex) => (
            <tr key={rowIndex}>
              {props.keys.map((key) => (
                <td key={key} style={{ border: '1px solid #ddd', padding: '8px' }}>
                  {key === 'Action' ? (
                    <button
                      className="btn btn-primary"
                      onClick={() => killProcess(group)}
                      disabled={!!killedItems[group.SID]}  // Disable if this SID is killed
                    >
                      {killedItems[group.SID] ? 'Killed' : 'Kill'}
                    </button>
                  ) : (
                    group[key]
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div>
      {renderTable(props.groupedData)}
    </div>
  );
}

print("hello")
