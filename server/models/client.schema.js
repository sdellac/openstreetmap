var Joi = require('joi');
 
var schema = Joi.object({
    client: Joi.object({
        id: Joi.string().required(),
        position: Joi.object({
            lat: Joi.number().required(),
            lon: Joi.number().required()
        }).required()
    }).required(),
    isServer: Joi.boolean()
});

module.exports = schema;
