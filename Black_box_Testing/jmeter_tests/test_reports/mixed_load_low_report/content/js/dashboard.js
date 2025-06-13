/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 99.87373737373737, "KoPercent": 0.12626262626262627};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.9974747474747475, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.9990723562152134, 500, 1500, "03_Product_Browse"], "isController": false}, {"data": [1.0, 500, 1500, "04_View_Cart"], "isController": false}, {"data": [1.0, 500, 1500, "03_Add_To_Cart"], "isController": false}, {"data": [0.9451219512195121, 500, 1500, "05_Place_Order"], "isController": false}, {"data": [0.9979338842975206, 500, 1500, "02_Product_Detail"], "isController": false}, {"data": [1.0, 500, 1500, "03_Add_To_Cart-0"], "isController": false}, {"data": [1.0, 500, 1500, "02_Static_CSS"], "isController": false}, {"data": [1.0, 500, 1500, "03_Add_To_Cart-1"], "isController": false}, {"data": [0.9968474148802018, 500, 1500, "01_Homepage"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 3168, 4, 0.12626262626262627, 14.445707070707055, 1, 1292, 10.0, 19.0, 22.0, 61.099999999999454, 10.608871534870637, 113.62193073069105, 3.447240967138619], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["03_Product_Browse", 539, 0, 0.0, 11.109461966604819, 7, 671, 9.0, 11.0, 15.0, 35.20000000000016, 1.8405201262070945, 14.695482914578013, 0.3522870554068267], "isController": false}, {"data": ["04_View_Cart", 240, 0, 0.0, 11.258333333333335, 8, 42, 10.0, 13.0, 16.94999999999999, 30.950000000000017, 0.840315538484701, 14.52401773350268, 0.14935295703536677], "isController": false}, {"data": ["03_Add_To_Cart", 242, 0, 0.0, 16.30991735537189, 11, 317, 14.0, 17.700000000000017, 21.0, 80.34999999999962, 0.8439995814878108, 14.657255273907507, 0.9618628042932375], "isController": false}, {"data": ["05_Place_Order", 82, 4, 4.878048780487805, 22.890243902439025, 11, 582, 15.5, 19.0, 25.69999999999999, 582.0, 0.305440187733969, 2.051990744836385, 0.15395687054178386], "isController": false}, {"data": ["02_Product_Detail", 242, 0, 0.0, 15.942148760330568, 7, 1169, 9.0, 11.0, 14.699999999999989, 241.66999999999774, 0.8452317751264354, 6.745628867066347, 0.16178264445779428], "isController": false}, {"data": ["03_Add_To_Cart-0", 242, 0, 0.0, 4.177685950413226, 3, 29, 4.0, 5.0, 5.0, 13.569999999999993, 0.8440260741278106, 0.07830320023646681, 0.5027889699394185], "isController": false}, {"data": ["02_Static_CSS", 546, 0, 0.0, 3.0586080586080566, 1, 78, 2.0, 3.0, 7.649999999999977, 12.0, 1.8446880754092267, 21.221118680000675, 0.3638935461256482], "isController": false}, {"data": ["03_Add_To_Cart-1", 242, 0, 0.0, 12.004132231404961, 8, 312, 10.0, 12.0, 13.849999999999994, 76.34999999999962, 0.8440290178571429, 14.579463005065916, 0.4591056278773716], "isController": false}, {"data": ["01_Homepage", 793, 0, 0.0, 27.498108448928143, 11, 1292, 18.0, 25.0, 35.299999999999955, 354.7399999999957, 2.655877930089791, 27.82833050190399, 0.4576106664646011], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["500/Internal Server Error", 4, 100.0, 0.12626262626262627], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 3168, 4, "500/Internal Server Error", 4, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["05_Place_Order", 82, 4, "500/Internal Server Error", 4, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
