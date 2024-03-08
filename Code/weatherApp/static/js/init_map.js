function initMap() {
    var map = L.map('map').setView([-27.07, 132.08], 4); // Latitude, Longitude, Zoom level when map first opens

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map); // Import and display map
    
    //Create markers for each city in database
    var albury = L.marker([-36.0751, 146.9095]).addTo(map);
    albury.bindPopup("<b>Albury</b><br>See wather details");
    var badgerys_creek = L.marker([-33.8751, 150.7634]).addTo(map);
    badgerys_creek.bindPopup("<b>Badgerys Creek</b><br>See wather details");
    var cobar = L.marker([-31.4978, 145.8363]).addTo(map);
    cobar.bindPopup("<b>Cobar</b><br>See wather details");
    var coffs_harbour = L.marker([-30.2962, 153.1139]).addTo(map);
    coffs_harbour.bindPopup("<b>Coffs Harbour</b><br>See wather details"); 
    var moree = L.marker([-29.4653, 149.8416]).addTo(map);
    moree.bindPopup("<b>Moree</b><br>See wather details");
    var newcastle = L.marker([-32.9283, 151.7817]).addTo(map);
    newcastle.bindPopup("<b>Newcastle</b><br>See wather details");
    var norah_head = L.marker([-33.2822, 151.5669]).addTo(map);
    norah_head.bindPopup("<b>Norah Head</b><br>See wather details");
    var norfolk_island = L.marker([-29.0408, 167.9547]).addTo(map);
    norfolk_island.bindPopup("<b>Norfolk Island</b><br>See wather details");
    var penrith = L.marker([-33.7507, 150.6877]).addTo(map);
    penrith.bindPopup("<b>Penrith</b><br>See wather details"); 
    var richmond = L.marker([-37.8239, 144.9983]).addTo(map);
    richmond.bindPopup("<b>Richmond</b><br>See wather details");
    var sydney = L.marker([-33.8688, 151.2093]).addTo(map);
    sydney.bindPopup("<b>Sydney</b><br>See wather details"); 
    var sydney_airport = L.marker([-33.9400, 151.1754]).addTo(map);
    sydney_airport.bindPopup("<b>Sydney Airport</b><br>See wather details");
    var wagga_wagga = L.marker([-35.1026, 147.3655]).addTo(map);
    wagga_wagga.bindPopup("<b>Wagga Wagga</b><br>See wather details"); 
    var williamtown = L.marker([-32.8115, 151.8443]).addTo(map);
    williamtown.bindPopup("<b>Williamtown</b><br>See wather details"); 
    var wollongong = L.marker([-34.4248, 150.8931]).addTo(map);
    wollongong.bindPopup("<b>Wollongong</b><br>See wather details"); 
    var canberra = L.marker([-35.2802, 149.1310]).addTo(map);
    canberra.bindPopup("<b>Canberra</b><br>See wather details"); 
    var tuggeranong = L.marker([-35.4180, 149.0694]).addTo(map);
    tuggeranong.bindPopup("<b>Tuggeranong</b><br>See wather details"); 
    var mount_ginini = L.marker([-35.5294, 148.7723]).addTo(map);
    mount_ginini.bindPopup("<b>Mount Ginini</b><br>See wather details"); 
    var ballarat = L.marker([-37.5622, 143.8503]).addTo(map);
    ballarat.bindPopup("<b>Ballarat</b><br>See wather details"); 
    var bendigo = L.marker([-36.7596, 144.2786]).addTo(map);
    bendigo.bindPopup("<b>Bendigo</b><br>See wather details");
    var sale = L.marker([-38.1051, 147.0680]).addTo(map);
    sale.bindPopup("<b>Sale</b><br>See wather details");
    var melbourne_airport = L.marker([-37.6708, 144.8430]).addTo(map);
    melbourne_airport.bindPopup("<b>Melbourne Airport</b><br>See wather details");
    var melbourne = L.marker([-37.8136, 144.9631]).addTo(map);
    melbourne.bindPopup("<b>Melbourne</b><br>See wather details"); 
    var mildura = L.marker([-34.2068, 142.1367]).addTo(map);
    mildura.bindPopup("<b>Mildura</b><br>See wather details"); 
    var nhil = L.marker([-36.3328, 141.6503]).addTo(map);
    nhil.bindPopup("<b>Nhil</b><br>See wather details"); 
    var portland = L.marker([-38.3421, 141.6012]).addTo(map);
    portland.bindPopup("<b>Portland</b><br>See wather details"); 
    var watsonia = L.marker([-37.7101, 145.0828]).addTo(map);
    watsonia.bindPopup("<b>Watsonia</b><br>See wather details");
    var dartmoor = L.marker([-37.9224, 141.2754]).addTo(map);
    dartmoor.bindPopup("<b>Dartmoor</b><br>See wather details");
    var brisbane = L.marker([-27.4705, 153.0260]).addTo(map);
    brisbane.bindPopup("<b>Brisbane</b><br>See wather details");
    var cairns = L.marker([-16.9203, 145.7710]).addTo(map);
    cairns.bindPopup("<b>Cairns</b><br>See wather details"); 
    var gold_coast = L.marker([-28.0167, 153.4000]).addTo(map);
    gold_coast.bindPopup("<b>Gold Coast</b><br>See wather details"); 
    var townsville = L.marker([-19.2590, 146.8169]).addTo(map);
    townsville.bindPopup("<b>Townsville</b><br>See wather details"); 
    var adelaide = L.marker([-34.9285, 138.6007]).addTo(map);
    adelaide.bindPopup("<b>Adelaide</b><br>See wather details"); 
    var mount_gambier = L.marker([-37.8284, 140.7807]).addTo(map);
    mount_gambier.bindPopup("<b>Mount Gambier</b><br>See wather details"); 
    var nuriootpa = L.marker([-34.4730, 138.9957]).addTo(map);
    nuriootpa.bindPopup("<b>Nuriootpa</b><br>See wather details"); 
    var woomera = L.marker([-31.1988, 136.8251]).addTo(map);
    woomera.bindPopup("<b>Woomera</b><br>See wather details"); 
    var albany = L.marker([-35.0268, 117.8837]).addTo(map);
    albany.bindPopup("<b>Albany</b><br>See wather details"); 
    var witch_cliffe = L.marker([-34.0262, 115.1002]).addTo(map);
    witch_cliffe.bindPopup("<b>Witch Cliffe</b><br>See wather details"); 
    var pearce_raaf = L.marker([-31.6676, 116.0292]).addTo(map);
    pearce_raaf.bindPopup("<b>Pearch RAAF</b><br>See wather details"); 
    var perth_airport = L.marker([-31.9385, 115.9672]).addTo(map);
    perth_airport.bindPopup("<b>Perth Airport</b><br>See wather details");
    var perth = L.marker([-31.9514, 115.8617]).addTo(map);
    perth.bindPopup("<b>Perth</b><br>See wather details"); 
    var salmon_gums = L.marker([-32.9804, 121.6456]).addTo(map);
    salmon_gums.bindPopup("<b>Salmon Gums</b><br>See wather details"); 
    var walpole = L.marker([-34.9762, 116.7313]).addTo(map);
    walpole.bindPopup("<b>Walpole</b><br>See wather details"); 
    var hobart = L.marker([-42.8826, 147.3257]).addTo(map);
    hobart.bindPopup("<b>Hobart</b><br>See wather details"); 
    var launceston = L.marker([-41.4391, 147.1358]).addTo(map);
    launceston.bindPopup("<b>Launceston</b><br>See wather details");
    var alice_springs = L.marker([-23.6980, 133.8807]).addTo(map);
    alice_springs.bindPopup("<b>Alice Springs</b><br>See wather details");
    var darwin = L.marker([-12.4637, 130.8444]).addTo(map);
    darwin.bindPopup("<b>Darwin</b><br>See wather details");
    var katherine = L.marker([-14.4520, 132.2699]).addTo(map);
    katherine.bindPopup("<b>Katherine</b><br>See wather details"); 
    var uluru = L.marker([-25.3444, 131.0369]).addTo(map);
    uluru.bindPopup("<b>Uluru</b><br>See wather details"); 

}

  initMap();
