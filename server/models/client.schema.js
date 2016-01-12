var Joi = require('joi');
 
var schema = Joi.object({
    client: Joi.object({
        ID: Joi.string().required(),
        Position: Joi.object({
            lat: Joi.number().min(-90).max(90).required(),
            lon: Joi.number().min(-180).max(180).required()
        }).required()
    }).required(),
    isServer: Joi.boolean()
});

module.exports = schema;
