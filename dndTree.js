
function createchart(){
    
    
    var par = document.getElementById('colltree');
    if(par != null){
        par.parentNode.removeChild(par);
    }
    
    var par2 = document.getElementById('sunchart');
    if(par2 != null){
        par2.parentNode.removeChild(par2);
        var  risultati = $('#risultati').DataTable();
        risultati.rows().remove().draw();

    }
    
    var a = document.getElementById('file1').value;
    var temp2 = a.split("jsonForChart");
    var b = "percentuali"+temp2[1];
    a = "jsonForChart"+temp2[1];

    
    /*
    let text;
    let file = document.querySelector("#file1").files[0];
    let reader = new FileReader();
    reader.addEventListener('load', function(e) {
          text = e.target.result;
          console.log("il testo è: ------ "+text);
    });
    reader.readAsText(file);
    */

    
// Get JSON data
//const params = new URLSearchParams(window.location.search)
//const filename = params.get('file')ss
//cdn.datatables.net/1.12.0/js/jquery.dataTables.min.js

jQuery.fn.d3Click = function()
{
    this.each(function(i,e){
    var evt = new MouseEvent("click");
    e.dispatchEvent(evt);
});
};



treeJSON = d3.json(a, function(error, treeData) {
    
   
    // Calculate total nodes, max label length
    var totalNodes = 0;
    var maxLabelLength = 0;
    // variables for drag/drop
    var selectedNode = null;
    var draggingNode = null;
    // panning variables
    var panSpeed = 100;
    var panBoundary = 20; // Within 20px from edges will pan when dragging.
    // Misc. variables
    var i = 0;
    var duration = 750;
    var root;

    // size of the diagram
    var viewerWidth = $("#contenitore").width();
    var viewerHeight = $(document).height();

    var tree = d3.layout.tree()
        .size([viewerHeight, viewerWidth]);
    // define a d3 diagonal projection for use by the node paths later on.
    var diagonal = d3.svg.diagonal()
        .projection(function(d) {
            return [d.y, d.x];
        });



    // A recursive helper function for performing some setup by walking through all nodes

    function visit(parent, visitFn, childrenFn) {
        if (!parent) return;

        visitFn(parent);

        var children = childrenFn(parent);
        if (children) {
            var count = children.length;
            for (var i = 0; i < count; i++) {
                visit(children[i], visitFn, childrenFn);
            }
        }
    }

    // Call visit function to establish maxLabelLength
    visit(treeData, function(d) {
        totalNodes++;
        maxLabelLength = Math.max(d.name.length, maxLabelLength);

    }, function(d) {
        return d.children && d.children.length > 0 ? d.children : null;
    });


    // sort the tree according to the node names

    function sortTree() {
        tree.sort(function(a, b) {
            return b.name.toLowerCase() < a.name.toLowerCase() ? 1 : -1;
        });
    }
    // Sort the tree initially incase the JSON isn't in a sorted order.
    sortTree();

    // TODO: Pan function, can be better implemented.

    function pan(domNode, direction) {
        var speed = panSpeed;
        if (panTimer) {
            clearTimeout(panTimer);
            translateCoords = d3.transform(svgGroup.attr("transform"));
            if (direction == 'left' || direction == 'right') {
                translateX = direction == 'left' ? translateCoords.translate[0] + speed : translateCoords.translate[0] - speed;
                translateY = translateCoords.translate[1];
            } else if (direction == 'up' || direction == 'down') {
                translateX = translateCoords.translate[0];
                translateY = direction == 'up' ? translateCoords.translate[1] + speed : translateCoords.translate[1] - speed;
            }
            scaleX = translateCoords.scale[0];
            scaleY = translateCoords.scale[1];
            scale = zoomListener.scale();
            svgGroup.transition().attr("transform", "translate(" + translateX + "," + translateY + ")scale(" + scale + ")");
            d3.select(domNode).select('g.node').attr("transform", "translate(" + translateX + "," + translateY + ")");
            zoomListener.scale(zoomListener.scale());
            zoomListener.translate([translateX, translateY]);
            panTimer = setTimeout(function() {
                pan(domNode, speed, direction);
            }, 50);
        }
    }

    // Define the zoom function for the zoomable tree

    function zoom() {
        svgGroup.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    }


    // define the zoomListener which calls the zoom function on the "zoom" event constrained within the scaleExtents
    var zoomListener = d3.behavior.zoom().scaleExtent([0.1, 10]).on("zoom", zoom);

    function initiateDrag(d, domNode) {
        draggingNode = d;
        d3.select(domNode).select('.ghostCircle').attr('pointer-events', 'none');
        d3.selectAll('.ghostCircle').attr('class', 'ghostCircle show');
        d3.select(domNode).attr('class', 'node activeDrag');

        svgGroup.selectAll("g.node").sort(function(a, b) { // select the parent and sort the path's
            if (a.id != draggingNode.id) return 1; // a is not the hovered element, send "a" to the back
            else return -1; // a is the hovered element, bring "a" to the front
        });

        // if nodes has children, remove the links and nodes
        if (nodes.length > 1) {
            // remove link paths
            links = tree.links(nodes);
            nodePaths = svgGroup.selectAll("path.link")
                .data(links, function(d) {
                    return d.target.id;
                }).remove();
            // remove child nodes
            nodesExit = svgGroup.selectAll("g.node")
                .data(nodes, function(d) {
                    return d.id;
                }).filter(function(d, i) {
                    if (d.id == draggingNode.id) {
                        return false;
                    }
                    return true;
                }).remove();
        }

        // remove parent link
        parentLink = tree.links(tree.nodes(draggingNode.parent));
        svgGroup.selectAll('path.link').filter(function(d, i) {
            if (d.target.id == draggingNode.id) {
                return true;
            }
            return false;
        }).remove();

        dragStarted = null;
    }

    // define the baseSvg, attaching a class for styling and the zoomListener
    var baseSvg = d3.select("#tree-container").append("svg")
        .attr("id", "colltree")
        .attr("width", viewerWidth)
        .attr("height", viewerHeight*0.8)
        .attr("class", "overlay")
        .call(zoomListener);



    // Helper functions for collapsing and expanding nodes.

    function collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    function expand(d) {
        if (d._children) {
            d.children = d._children;
            d.children.forEach(expand);
            d._children = null;
        }
    }

    var overCircle = function(d) {
        selectedNode = d;
        updateTempConnector();
    };
    var outCircle = function(d) {
        selectedNode = null;
        updateTempConnector();
    };

    // Function to update the temporary connector indicating dragging affiliation
    var updateTempConnector = function() {
        var data = [];
        if (draggingNode !== null && selectedNode !== null) {
            // have to flip the source coordinates since we did this for the existing connectors on the original tree
            data = [{
                source: {
                    x3: selectedNode.y0,
                    y3: selectedNode.x0
                },
                target: {
                    x: draggingNode.y0,
                    y: draggingNode.x0
                }
            }];
        }
        var link = svgGroup.selectAll(".templink").data(data);

        link.enter().append("path")
            .attr("class", "templink")
            .attr("d", d3.svg.diagonal())
            .attr('pointer-events', 'none');

        link.attr("d", d3.svg.diagonal());

        link.exit().remove();
    };

    // Function to center node when clicked/dropped so node doesn't get lost when collapsing/moving with large amount of children.

    function centerNode(source) {
        scale = zoomListener.scale();
        x2p = -source.y0;
        y2p = -source.x0;
        x2p = x2p * scale + viewerWidth / 2;
        y2p = y2p * scale + viewerHeight / 2;
        d3.select('g').transition()
            .duration(duration)
            .attr("transform", "translate(" + x2p + "," + y2p + ")scale(" + scale + ")");
        zoomListener.scale(scale);
        zoomListener.translate([x2p, y2p]);
    }

    // Toggle children function

    function toggleChildren(d) {

        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else if (d._children) {
            d.children = d._children;
            d._children = null;
        }
        return d;
    }

    // Toggle children on click.

    function click(d) {
        if (d3.event.defaultPrevented) return; // click suppressed
        if (d.name == "new RFDs") {
            var  risultati = $('#risultati').DataTable();
            var lista = d._children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){  
                $("#new_RFDs").d3Click();          
                for(let i=0; i<lista.length; i++){
                    var listalhs = lista[i]._children;
                    if(listalhs != null){
                        for (let j = 0; j<listalhs.length;j++) {                        
                            risultati.row.add(["nd","nd","new RFD",""+listalhs[j].name, ""+lista[i].name]).draw(false);                
                        }    
                    }
                    else{
                       lista[i]._children = lista[i].children;
                       lista[i].children = null;
                       var listalhs = lista[i]._children;
                        update(lista[i]);
                        for (let j = 0; j<listalhs.length;j++) {                        
                            risultati.row.add(["nd","nd","new RFD",""+listalhs[j].name, ""+lista[i].name]).draw(false);                
                        }    
                    }
                }
            } else {
                $("#RFDs").d3Click();
               var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "new RFD";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               lista2 = d._children;
               for (let j = 0; j<lista2.length;j++) {
                   filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "new RFD: "+lista2[j].name+"  ";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               }
            } 
        } else if (d.name == "RFD found") {
            var  risultati = $('#risultati').DataTable();
            var lista = d._children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){ 
                $("#RFD_found").d3Click();           
                for(let i=0; i<lista.length; i++){
                    var listalhs = lista[i]._children;
                    
                    if(listalhs != null){
                        for (let j = 0; j<listalhs.length;j++) {
                            risultati.row.add([""+listalhs[j].name,""+lista[i].name,"RFD found",""+listalhs[j].name, ""+lista[i].name]).draw(false);                

                        }    
                    } else{
                        lista[i]._children = lista[i].children;
                        lista[i].children = null;
                        var listalhs = lista[i]._children;
                        update(lista[i]);
                        for (let j = 0; j<listalhs.length;j++) {                        
                            risultati.row.add([""+listalhs[j].name,""+lista[i].name,"RFD found",""+listalhs[j].name, ""+lista[i].name]).draw(false);                
                        }    
                    }    
                }
            } else {
                $("#RFDs").d3Click();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "RFD found";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               lista2 = d._children;
               for (let j = 0; j<lista2.length;j++) {
                   filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "RFD found: "+lista2[j].name+"  ";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               }
                
            }  
        } else if (d.name == "RFD not found") {
            
            var  risultati = $('#risultati').DataTable();
            var lista = d._children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){
                $("#RFD_not_found").d3Click();            
                for(let i=0; i<lista.length; i++){
                    var listalhs = lista[i]._children;
                    if(listalhs != null){
                        for (let j = 0; j<listalhs.length;j++) {
                            risultati.row.add([""+listalhs[j].name,""+lista[i].name,"RFD not found","nd","nd"]).draw(false);                         
                        }
                    } else {
                        lista[i]._children = lista[i].children;
                        lista[i].children = null;
                        var listalhs = lista[i]._children;
                        update(lista[i]);
                        for (let j = 0; j<listalhs.length;j++) {                        
                            risultati.row.add([""+listalhs[j].name,""+lista[i].name,"RFD not found","nd","nd"]).draw(false);                         
                        }  
                    }    
                }
            } else {
                $("#RFDs").d3Click();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "RFD not found";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               lista2 = d._children;
               for (let j = 0; j<lista2.length;j++) {
                   filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "RFD not found: "+lista2[j].name+"  ";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               }
            }

        } else if (d.name == "generalizations") {
            
            var  risultati = $('#risultati').DataTable();
            var lista = d._children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){
                if(lista.length!=0){
                 $("#generalizations").d3Click();    
                }         
                for(let i=0; i<lista.length; i++){
                    var listalhs = lista[i]._children;
                    if(listalhs != null){
                        for (let j = 0; j<listalhs.length;j++) {
                            risultati.row.add(["nd","nd","generalizations",""+listalhs[j].name, ""+lista[i].name]).draw(false);                
                        }
                    } else {
                        lista[i]._children = lista[i].children;
                        lista[i].children = null;
                        var listalhs = lista[i]._children;
                        update(lista[i]);
                        for (let j = 0; j<listalhs.length;j++) {                        
                            risultati.row.add(["nd","nd","generalizations",""+listalhs[j].name, ""+lista[i].name]).draw(false);                
                        }   
                    }   
                }
            } else {
                $("#RFDs").d3Click();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "generalizations";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               lista2 = d._children;
               for (let j = 0; j<lista2.length;j++) {
                   filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "generalizations: "+lista2[j].name;  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               }
            }  

        } else if (d.name == "specializations") {
            
            var  risultati = $('#risultati').DataTable();
            var lista = d._children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){            
                $("#specializations").d3Click();
                for(let i=0; i<lista.length; i++){
                    var listalhs = lista[i]._children;
                    if(listalhs != null){
                        for (let j = 0; j<listalhs.length;j++) { 
                            risultati.row.add(["nd","nd","specializations",""+listalhs[j].name, ""+lista[i].name]).draw(false);                
                        }
                    } else {
                      lista[i]._children = lista[i].children;
                        lista[i].children = null;
                        var listalhs = lista[i]._children;
                        update(lista[i]);
                        for (let j = 0; j<listalhs.length;j++) {                        
                            risultati.row.add(["nd","nd","specializations",""+listalhs[j].name, ""+lista[i].name]).draw(false);                
                        }  
                    }    
                }
            } else {
                $("#RFDs").d3Click();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "specializations";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               lista2 = d._children;
               for (let j = 0; j<lista2.length;j++) {
                   filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "specializations: "+lista2[j].name;  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
               }
            }  
        } 
        else if (d.parent.name == "RFD found") {
            var  risultati = $('#risultati').DataTable();
            var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "RFD found";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
            var lista = d._children;
            var parente = d.parent;
            var figli = parente.children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);            
            if(lista != null){
                var nomepath = "#RFD_found"+d.name;
                $(nomepath).d3Click();
            
                for(let i=0; i<lista.length; i++){
                    var listalhs = lista[i]._children;
                    
                    for (let j = 0; j<listalhs.length;j++) {
                        var myArray = listalhs[j].name.split("LHS:");
                        var word = myArray[0];
                        myArray=word.split("RHS: ");
                        word=myArray[1];
                        risultati.row.add([""+lista[i].name,""+word,"RFD found: "+word,""+lista[i].name, ""+word]).draw(false);                        
                    }    
                }
            } else {
                $("#RFD_found").d3Click();
                risultati = $('#risultati').DataTable();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                                var confronto = "RFD found: "+ d.name+"  ";
                               return risultati.row(value).data()[2] == confronto;  
                            } );
                        risultati.rows( filteredData ).remove().draw();
                if (!risultati.data().any() ) {
                    for(let i=0; i<figli.length; i++){
                    var listalhs = figli[i]._children;
                    
                    for (let j = 0; j<listalhs.length;j++) {
                            risultati.row.add(["nd","nd","RFD found",""+listalhs[j].name, ""+figli[i].name]).draw(false);    
                    }    
                }
                }         
            }
        } else if (d.parent.name == "new RFDs") {
            var  risultati = $('#risultati').DataTable();
            var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "new RFD";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
            var lista = d._children;
            var parente = d.parent;
            var figli = parente.children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){
                var nomepath = "#new_RFDs"+d.name;
                $(nomepath).d3Click();
            
                for(let i=0; i<lista.length; i++){
                    var listalhs = lista[i]._children;
                    
                    for (let j = 0; j<listalhs.length;j++) {
                        var myArray = listalhs[j].name.split("LHS:");
                        var word = myArray[0];
                        myArray=word.split("RHS: ");
                        word=myArray[1];
                        risultati.row.add(["nd","nd","new RFD: "+word,""+lista[i].name,""+word]).draw(false);                         
                    }    
                }
            } else {
                $("#new_RFDs").d3Click();
                risultati = $('#risultati').DataTable();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                                var confronto = "new RFD: "+ d.name+"  ";
                               return risultati.row(value).data()[2] == confronto;  
                            } );
                        risultati.rows( filteredData ).remove().draw();
                if (!risultati.data().any() ) {
                    for(let i=0; i<figli.length; i++){
                    var listalhs = figli[i]._children;
                    
                    for (let j = 0; j<listalhs.length;j++) {
                            risultati.row.add(["nd","nd","new RFD",""+listalhs[j].name, ""+figli[i].name]).draw(false);    
                    }    
                }
                }
            }
        } else if (d.parent.name == "RFD not found") {
            var  risultati = $('#risultati').DataTable();
            var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "RFD not found";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
            var lista = d._children;
            var parente = d.parent;
            var figli = parente.children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){
                var nomepath = "#RFD_not_found"+d.name;
                $(nomepath).d3Click();
            
                for(let i=0; i<lista.length; i++){
                    var listalhs = lista[i]._children;
                    
                    for (let j = 0; j<listalhs.length;j++) {
                        var myArray = listalhs[j].name.split("LHS:");
                        var word = myArray[0];
                        myArray=word.split("RHS: ");
                        word=myArray[1];
                        risultati.row.add([""+lista[i].name,""+word,"RFD not found: "+word,"nd","nd"]).draw(false);                            
                    }    
                }
            } else {
              $("#RFD_not_found").d3Click();
              risultati = $('#risultati').DataTable();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                                var confronto = "RFD not found: "+ d.name+"  ";
                               return risultati.row(value).data()[2] == confronto;  
                            } );
                        risultati.rows( filteredData ).remove().draw();
                if (!risultati.data().any() ) {
                    for(let i=0; i<figli.length; i++){
                    var listalhs = figli[i]._children;
                    
                    for (let j = 0; j<listalhs.length;j++) {
                        risultati.row.add([""+listalhs[j].name,figli[i].name,"RFD not found","nd","nd"]).draw(false);                            
                    }    
                }
                }  
            }

        }else if (d.parent.name == "specializations") {
            var  risultati = $('#risultati').DataTable();
            var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "specializations";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
            var lista = d._children;
            var parente = d.parent;
            var figli = parente.children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){
                var nomepath = "#specializations"+d.name;
                $(nomepath).d3Click();
                for(let i=0; i<lista.length; i++){                   
                    var listalhs = lista[i]._children;   
                    for (let j = 0; j<listalhs.length;j++) {

                        var myArray = listalhs[j].name.split("LHS:");
                        var word = myArray[1];
                        risultati.row.add([""+word,""+d.name,"specializations: "+d.name,""+lista[i].name, ""+d.name]).draw(false);                         

                    }    
                }
            } else {
                $("#specializations").d3Click();
                risultati = $('#risultati').DataTable();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {   
                    var confronto = "specializations: "+ d.name;
                    return risultati.row(value).data()[2] == confronto;  
                } );
                risultati.rows( filteredData ).remove().draw();
                for (let i = 0; i<figli.length;i++) {
                    var figlidifiglio = figli[i]._children;
                    for(let j = 0; j<figlidifiglio.length; j++){
                        risultati.row.add(["nd","nd","specializations",""+figlidifiglio[j].name, ""+figli[i].name]).draw(false);
                    }
                }   
            }
        } else if (d.parent.name == "generalizations") {
             var  risultati = $('#risultati').DataTable();
            var filteredData = risultati.rows().indexes().filter( function ( value, index ) {
                               return risultati.row(value).data()[2] == "generalizations";  
                            } );
                        risultati.rows( filteredData )
                        .remove()
                        .draw();
            var lista = d._children;
            var parente = d.parent;
            var figli = parente.children;
            d = toggleChildren(d);
            update(d);
            centerNode(d);
            if(lista != null){
                var nomepath = "#generalizations"+d.name;
                $(nomepath).d3Click();
                for(let i=0; i<lista.length; i++){                   
                    var listalhs = lista[i]._children;   
                    for (let j = 0; j<listalhs.length;j++) {

                        var myArray = listalhs[j].name.split("LHS:");
                        var word = myArray[1];
                        risultati.row.add([""+word,""+d.name,"",""+lista[i].name, ""+d.name]).draw(false);                         
                    }    
                }
            } else {

                $("#generalizations").d3Click();
                risultati = $('#risultati').DataTable();
                var filteredData = risultati.rows().indexes().filter( function ( value, index ) {   
                    var confronto = "generalizations: "+ d.name;
                    return risultati.row(value).data()[2] == confronto;  
                } );
                risultati.rows( filteredData ).remove().draw();
                for (let i = 0; i<figli.length;i++) {
                    var figlidifiglio = figli[i]._children;
                    for(let j = 0; j<figlidifiglio.length; j++){
                        risultati.row.add(["nd","nd","generalizations",""+figlidifiglio[j].name, ""+figli[i].name]).draw(false);
                    }
                }   
            }
        } 
    }


    function update(source) {
        // Compute the new height, function counts total children of root node and sets tree height accordingly.
        // This prevents the layout looking squashed when new nodes are made visible or looking sparse when nodes are removed
        // This makes the layout more consistent.
        var levelWidth = [1];
        var childCount = function(level, n) {

            if (n.children && n.children.length > 0) {
                if (levelWidth.length <= level + 1) levelWidth.push(0);

                levelWidth[level + 1] += n.children.length;
                n.children.forEach(function(d) {
                    childCount(level + 1, d);
                });
            }
        };
        childCount(0, root);
        var newHeight = d3.max(levelWidth) * 25; // 25 pixels per line  
        tree = tree.size([newHeight, viewerWidth]);

        // Compute the new tree layout.
        var nodes = tree.nodes(root).reverse(),
            links = tree.links(nodes);

        // Set widths between levels based on maxLabelLength.
        nodes.forEach(function(d) {
            var tmp = 3;
            if(d.depth == 3)
                tmp = 4
            d.y = (d.depth * (maxLabelLength * tmp)); //maxLabelLength * 10px
            // alternatively to keep a fixed scale one can set a fixed depth per level
            // Normalize for fixed-depth by commenting out below line
            // d.y = (d.depth * 500); //500px per level.
        });

        // Update the nodes…
        node = svgGroup.selectAll("g.node")
            .data(nodes, function(d) {
                return d.id || (d.id = ++i);
            });

        // Enter any new nodes at the parent's previous position.
        var nodeEnter = node.enter().append("g")
            //.call(dragListener)
            .attr("class", "node")
            .attr("transform", function(d) {
                return "translate(" + source.y0 + "," + source.x0 + ")";
            })
            .on('click', click)
            .attr("id",function(d) {
                if(d.name=="RFDs"||d.name=="specializations"||d.name=="generalizations"||d.name=="new RFDs"||d.name=="RFD not found"||d.name=="RFD found"){
                    var nom = "tree"+d.name;
                    var finale = nom.replaceAll(" ","_");
                    return finale;
                } else {
                    var nom = "tree"+d.parent.name+""+d.name;
                    var finale = nom.replaceAll(" ","_");
                    return finale;
                }
            });

        nodeEnter.append("circle")
            .attr('class', 'nodeCircle')
            .attr("r", 0)
            .style("fill", function(d) {
                return d._children ? "lightsteelblue" : "#fff";
            })
            

        nodeEnter.append("text")
            .attr("x", function(d) {
                return d.children || d._children ? -10 : 10;
            })
            .attr("dy", ".35em")
            .attr('class', 'nodeText')
            .attr("text-anchor", function(d) {
                if(d.depth == 3){
                    return "middle";
                }
                return d.children || d._children ? "end" : "start";
            })
            .text(function(d) {
                return d.name;
            })
            .style("fill-opacity", 0);

        // phantom node to give us mouseover in a radius around it
        nodeEnter.append("circle")
            .attr('class', 'ghostCircle')
            .attr("r", 30)
            .attr("opacity", 0.2) // change this to zero to hide the target area
            .style("fill", "red")
            .attr('pointer-events', 'mouseover')
            .on("mouseover", function(node) {
                overCircle(node);
            })
            .on("mouseout", function(node) {
                outCircle(node);
            });

        // Update the text to reflect whether node has children or not.
        node.select('text')
            .attr("x", function(d) {
                return d.children || d._children ? -10 : 10;
            })
            .attr("dx", function(d) {
                if(d.depth == 3){
                    return "1.35em";
                }
            })
            .attr("text-anchor", function(d) {
                if(d.depth == 3){
                    return "left";
                }
                return d.children || d._children ? "end" : "start";
            })
            .text(function(d) {
                return d.name;
            });

        // Change the circle fill depending on whether it has children and is collapsed
        node.select("circle.nodeCircle")
            .attr("r", 4.5)
            .style("fill", function(d) {
                return d._children ? "lightsteelblue" : "#fff";
            });

        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + d.y + "," + d.x + ")";
            });

        // Fade the text in
        nodeUpdate.select("text")
            .style("fill-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.y3 + "," + source.x3 + ")";
            })
            .remove();

        nodeExit.select("circle")
            .attr("r", 0);

        nodeExit.select("text")
            .style("fill-opacity", 0);

        // Update the links…
        var link = svgGroup.selectAll("path.link")
            .data(links, function(d) {
                return d.target.id;
            });

        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", function(d) {
                var o = {
                    x: source.x0,
                    y: source.y0
                };
                return diagonal({
                    source: o,
                    target: o
                });
            });

        // Transition links to their new position.
        link.transition()
            .duration(duration)
            .attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(duration)
            .attr("d", function(d) {
                var o = {
                    x: source.x3,
                    y: source.y3
                };
                return diagonal({
                    source: o,
                    target: o
                });
            })
            .remove();

        // Stash the old positions for transition.
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }

    // Append a group which holds all nodes and which the zoom Listener can act upon.
    var svgGroup = baseSvg.append("g");

    // Define the root
    root = treeData;
    root.x0 = viewerHeight / 2;
    root.y0 = 0;
	
	// Collapse all children of roots children before rendering.
	root.children.forEach(function(child){
		collapse(child);
	});

    // Layout the tree initially and center on the root node.
    update(root);
    centerNode(root);
});


}


