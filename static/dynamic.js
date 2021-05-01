window.setInterval(function () {
    get_stock()
    }, 3000);

function get_stock(){
    /* Variables that stores stock information to display dynamically
    companyName : The full company name
    ticker: The company Symbol(ticker)
    quote:  The company current stock quote in USD*/
    var companyName;
    var ticker;
    var quote;

    $.ajax({
        type: "GET",
        url: "/stock_info" ,
        contentType: false,
        processData: false,
        success: function (jsonresult) {
            console.log(jsonresult);
            var obj = jsonresult;
            companyName = obj.stocks.simple_name;
            ticker = obj.stocks.symbol;
            quote = parseInt(obj.stocks.stockPrice).toFixed(2);
            remove_stock();
            add_stock(companyName,ticker,quote);
            console.log("THE COMPANY NAME",companyName);
        },
        error:function(error){
            console.log(`Error ${error}`)
        }
    });
}

function add_stock(companyName,ticker,quote){

var stockScene = document.querySelector('#stock-card');
var stockTicker = document.createElement('a-entity');
stockTicker.setAttribute('id','stock-ticker');
var buyButton = document.querySelector('#buybutton');

// AFRAME.registerComponent('do-something-once-loaded', {
//     update: function () {
//         console.log('Updating');
//       }
//     });

stockTicker.setAttribute('position','0.0.5 0.2 0.1');
stockTicker.setAttribute('material',{
    color: "#21c995",
}
);
stockTicker.setAttribute('geometry',{
    primitive: 'plane',
    width: '0.2',
    height: '0.075',
})
// The text attribute that displays the Stock ticker
stockTicker.setAttribute('text', {
    width:1,
    font:'exo2semibold',
    value: `${companyName}\n ${ticker}`,
    color: '#212121',
    align: 'center',
});
let insertTicker = stockScene.insertBefore(stockTicker,buyButton);

var stockQuote = document.createElement('a-text');
stockQuote.setAttribute('id','stock-quote');

stockQuote.setAttribute('font','kelsonsans');
stockQuote.setAttribute('position',"-0.06 0.05 0.2");
stockQuote.setAttribute('color',"#212121");
stockQuote.setAttribute('align',"center");
stockQuote.setAttribute('height',0.2);
stockQuote.setAttribute('width',0.8);
stockQuote.setAttribute('value',`$ ${quote}`);

let insertQuote = stockScene.insertBefore(stockQuote,buyButton);
}

function remove_stock(){
var stockTicker = document.getElementById('stock-ticker');
var stockQuote = document.getElementById('stock-quote');

if(stockTicker != null && stockQuote != null){
stockTicker.parentNode.removeChild(stockTicker);
stockQuote.parentNode.removeChild(stockQuote);

}
}



