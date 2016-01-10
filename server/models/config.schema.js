var Joi = require('joi');
 
var schema = Joi.object({
    servers: Joi.array(
        Joi.object({
            host: Joi.string().regex(/[^\:]+(:[0-9]+)?/).required(),
            zone: Joi.object({
                minlat: Joi.number().required(),
                maxlat: Joi.number().required(),
                minlon: Joi.number().required(),
                maxlon: Joi.number().required()
            }).required()
        }).required()
    ).required()
});

module.exports = schema;
