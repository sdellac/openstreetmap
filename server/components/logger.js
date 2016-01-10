var winston = require('winston');

var logger = module.exports = new (winston.Logger)({
  transports: [
    new (winston.transports.Console)({
      colorize: 'all',
      timestamp: true
    })
  ]
});
