const path = require('path')

module.exports = {
  entry: path.join(__dirname,'script.js'),
  output: {
    path: path.join(__dirname, 'dist/'),
    filename: 'app.js'
  },
}