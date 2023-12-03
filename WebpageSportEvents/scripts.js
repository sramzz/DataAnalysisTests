async function export_fixtures_to_csv(country, start_date, end_date) {
    const url = "https://api.fixturecalendar.com/api/v1/fixtures";
    const params = new URLSearchParams({
      country: country,
      startDate: start_date,
      endDate: end_date,
    });
  
    const response = await fetch(`${url}?${params}`, {
      headers: {
        accept: "application/json",
      },
    });
  
    let csvData = "";
  
    if (response.status === 200) {
      const allfixtures = await response.json();
  
      const dict_event = {
        date: [],
        name: [],
        location: [],
        sport: [],
        competition: [],
      };
  
      for (const event of allfixtures["events"]) {
        dict_event["date"].push(event["startTime"]);
        dict_event["name"].push(event["cachedFrontEndName"]);
        dict_event["location"].push(event["location"]["address"]);
        dict_event["sport"].push(event["sport"]["name"]);
        dict_event["competition"].push(event["competition"]["name"]);
      }
  
      const headerRow = Object.keys(dict_event).join(",") + "\n";
      csvData += headerRow;
  
      const numberOfRows = dict_event["date"].length;
      for (let i = 0; i < numberOfRows; i++) {
        let row = "";
        for (const key in dict_event) {
          row += `"${dict_event[key][i]}",`;
        }
        row = row.slice(0, -1); // Remove the trailing comma
        row += "\n";
        csvData += row;
      }
    } else {
      console.error("Failed to get data. Error code:", response.status);
    }
  
    return csvData;
  }
  
  document.getElementById("downloadForm").addEventListener("submit", async (event) => {
    event.preventDefault();
  
    const country = document.getElementById("country").value;
    const start_date = document.getElementById("start_date").value;
    const end_date = document.getElementById("end_date").value;
  
    const csvData = await export_fixtures_to_csv(country, start_date, end_date);
    createTable(csvData);
  
    const downloadLink = document.createElement("a");
    downloadLink.href = `data:text/csv;charset=utf-8,${encodeURIComponent(csvData)}`;
    downloadLink.download = `events${country}${start_date}_${end_date}.csv`;
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  });
  
  function createTable(csvData) {
    const tableWrapper = document.getElementById("tableWrapper");
    tableWrapper.innerHTML = "";
  
    const table = document.createElement("table");
    table.classList.add("w-full", "text-text", "bg-secondary", "rounded", "overflow-hidden");
  
    const lines = csvData.split("\n");
    for (const line of lines) {
      const row = document.createElement("tr");
      const values = line.split(",");
  
      for (const value of values) {
        const cell = document.createElement("td");
        cell.textContent = value.replace(/"/g, ""); // Remove quotes from the CSV values
        row.appendChild(cell);
      }
  
      table.appendChild(row);
    }
  
    tableWrapper.appendChild(table);
  };