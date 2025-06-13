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

    var data = {"OkPercent": 99.8976819673288, "KoPercent": 0.10231803267120629};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.6942190311540768, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.7546239837398374, 500, 1500, "03_Product_Browse"], "isController": false}, {"data": [0.5717798594847775, 500, 1500, "04_View_Cart"], "isController": false}, {"data": [0.523859649122807, 500, 1500, "03_Add_To_Cart"], "isController": false}, {"data": [0.7676450034940601, 500, 1500, "05_Place_Order"], "isController": false}, {"data": [0.7596917328351238, 500, 1500, "02_Product_Detail"], "isController": false}, {"data": [0.9895906432748538, 500, 1500, "03_Add_To_Cart-0"], "isController": false}, {"data": [0.9998985698346688, 500, 1500, "02_Static_CSS"], "isController": false}, {"data": [0.5826900584795321, 500, 1500, "03_Add_To_Cart-1"], "isController": false}, {"data": [0.4453769659355385, 500, 1500, "01_Homepage"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 56686, 58, 0.10231803267120629, 648.208887556011, 1, 7406, 599.0, 1292.0, 1436.0, 1854.9600000000064, 63.046440110553156, 678.0186030586326, 20.387213224948976], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["03_Product_Browse", 9840, 0, 0.0, 556.0986788617871, 8, 6971, 494.0, 800.0, 959.9499999999989, 1355.3100000000013, 10.979349004940707, 87.63976785727237, 2.1015160204769323], "isController": false}, {"data": ["04_View_Cart", 4270, 0, 0.0, 739.0585480093687, 9, 6812, 708.0, 1078.9, 1217.4499999999998, 1559.0, 4.78534317746787, 83.80766944401485, 0.850519978807766], "isController": false}, {"data": ["03_Add_To_Cart", 4275, 0, 0.0, 878.8760233918133, 12, 7406, 831.0, 1295.0, 1492.3999999999996, 1986.7199999999993, 4.788612176180603, 84.29209387003034, 5.457334384377699], "isController": false}, {"data": ["05_Place_Order", 1431, 58, 4.053109713487072, 507.05520614954526, 9, 7125, 444.0, 811.9999999999998, 986.5999999999995, 1565.2000000000057, 1.620580351227666, 10.909778103082953, 0.8165121856374226], "isController": false}, {"data": ["02_Product_Detail", 4282, 0, 0.0, 531.503970107427, 8, 7018, 490.0, 792.0, 936.8499999999999, 1252.8500000000004, 4.789077056943267, 38.213541209395736, 0.9166592804305471], "isController": false}, {"data": ["03_Add_To_Cart-0", 4275, 0, 0.0, 126.93567251461982, 2, 1872, 98.0, 246.0, 303.1999999999998, 700.6399999999976, 4.790796291979703, 0.4444586403692107, 2.8538923223707213], "isController": false}, {"data": ["02_Static_CSS", 9859, 0, 0.0, 62.58190485850484, 1, 604, 55.0, 119.0, 172.0, 250.0, 10.987063816129666, 126.39415210352291, 2.1673700106037037], "isController": false}, {"data": ["03_Add_To_Cart-1", 4275, 0, 0.0, 751.7974269005839, 8, 6903, 701.0, 1101.0, 1213.1999999999998, 1603.0, 4.78866581609507, 83.84877708396576, 2.6047723237939007], "isController": false}, {"data": ["01_Homepage", 14179, 0, 0.0, 1197.8494957331316, 11, 2780, 1199.0, 1615.0, 1789.0, 2183.2000000000007, 15.76995156348187, 165.23907254459942, 2.7345270592471485], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["500/Internal Server Error", 58, 100.0, 0.10231803267120629], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 56686, 58, "500/Internal Server Error", 58, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["05_Place_Order", 1431, 58, "500/Internal Server Error", 58, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
