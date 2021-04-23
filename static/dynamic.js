/* Variables that stores stock information to display dynamically
companyName : The full company name
ticker: The company Symbol(ticker)
quote:  The company current stock quote in USD*/
var companyName = "STARBUCKS";
var ticker = "SMPL";
var quote = 65.12;


var stockScene = document.querySelector('#stock-card');
var stockTicker = document.createElement('a-entity');
var buyButton = document.querySelector('#buybutton');

AFRAME.registerComponent('do-something-once-loaded', {
    init: function () {
        // This will be called after the entity has properly attached and loaded.
        console.log('I am ready!');
        // stockTicker.setAttribute('material','color', 'red')
    }
    });

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

stockQuote.setAttribute('font','kelsonsans');
stockQuote.setAttribute('position',"-0.06 0.05 0.2");
stockQuote.setAttribute('color',"#212121");
stockQuote.setAttribute('align',"center");
stockQuote.setAttribute('height',0.2);
stockQuote.setAttribute('width',0.8);
stockQuote.setAttribute('value',`$ ${quote}`);

let insertQuote = stockScene.insertBefore(stockQuote,buyButton);


