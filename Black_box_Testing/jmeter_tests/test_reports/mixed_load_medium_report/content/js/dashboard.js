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

    var data = {"OkPercent": 99.88860007426662, "KoPercent": 0.11139992573338285};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.9622301204180149, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.9700276667691362, 500, 1500, "03_Product_Browse"], "isController": false}, {"data": [0.9568421052631579, 500, 1500, "04_View_Cart"], "isController": false}, {"data": [0.944327731092437, 500, 1500, "03_Add_To_Cart"], "isController": false}, {"data": [0.9159663865546218, 500, 1500, "05_Place_Order"], "isController": false}, {"data": [0.970979020979021, 500, 1500, "02_Product_Detail"], "isController": false}, {"data": [0.9856442577030813, 500, 1500, "03_Add_To_Cart-0"], "isController": false}, {"data": [0.9970921334557699, 500, 1500, "02_Static_CSS"], "isController": false}, {"data": [0.9695378151260504, 500, 1500, "03_Add_To_Cart-1"], "isController": false}, {"data": [0.9324639525021204, 500, 1500, "01_Homepage"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 18851, 21, 0.11139992573338285, 132.23441727229408, 1, 6582, 22.0, 318.0, 605.3999999999978, 1570.9199999999983, 31.531584273515712, 339.40153018340874, 10.212523077678997], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["03_Product_Browse", 3253, 0, 0.0, 118.3147863510606, 7, 3774, 22.0, 267.5999999999999, 533.2999999999997, 1221.38, 5.475177400460501, 43.7253798214971, 1.0479831743068928], "isController": false}, {"data": ["04_View_Cart", 1425, 0, 0.0, 158.3312280701752, 8, 4526, 35.0, 373.0, 633.3000000000004, 1935.8200000000004, 2.421669609490906, 42.4553567066228, 0.43041393449936016], "isController": false}, {"data": ["03_Add_To_Cart", 1428, 0, 0.0, 188.14495798319297, 11, 5116, 47.0, 464.10000000000014, 798.1999999999998, 1941.970000000004, 2.4197278992254496, 42.64326115894037, 2.7576391195274415], "isController": false}, {"data": ["05_Place_Order", 476, 21, 4.411764705882353, 165.18067226890744, 9, 4676, 33.5, 357.3, 748.5999999999995, 2345.640000000003, 0.8292162860865869, 5.5781868700308, 0.4177962325098078], "isController": false}, {"data": ["02_Product_Detail", 1430, 0, 0.0, 114.92307692307686, 7, 3606, 21.0, 268.9000000000001, 527.45, 1277.38, 2.4180361826141508, 19.30161483441948, 0.4628272380784898], "isController": false}, {"data": ["03_Add_To_Cart-0", 1428, 0, 0.0, 56.16526610644263, 2, 2619, 5.0, 95.0, 251.19999999999982, 846.4200000000001, 2.420150293366958, 0.2245256619822861, 1.4416910927283635], "isController": false}, {"data": ["02_Static_CSS", 3267, 0, 0.0, 25.895622895622864, 1, 2475, 3.0, 64.0, 82.0, 275.6000000000008, 5.487611301758152, 63.12896595186624, 1.0825170731983855], "isController": false}, {"data": ["03_Add_To_Cart-1", 1428, 0, 0.0, 131.87815126050435, 8, 2842, 21.0, 310.0, 500.0, 1600.42, 2.419764801572508, 42.419421596464396, 1.3162197211678586], "isController": false}, {"data": ["01_Homepage", 4716, 0, 0.0, 215.7521204410515, 11, 6582, 49.0, 552.0, 956.4499999999989, 2342.9399999999987, 7.888332260033955, 82.65774985311828, 1.3661502458831303], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["500/Internal Server Error", 21, 100.0, 0.11139992573338285], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 18851, 21, "500/Internal Server Error", 21, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["05_Place_Order", 476, 21, "500/Internal Server Error", 21, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
