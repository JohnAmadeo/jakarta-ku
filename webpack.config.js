var webpack = require('webpack');  
module.exports = {  
  entry: {
    "index": "./static/js/index.js"
  },
  output: {
    path: __dirname + '/static/dist',
    filename: "[name].js"
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
  ]
};