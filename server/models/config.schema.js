var Joi = require('joi');
 
var schema = Joi.object({
    servers: Joi.array(
        Joi.object({
            host: Joi.string().regex(/[^\:]+(:[0-9]+)?/).required(),
            zone: Joi.object({
                minlat: Joi.number().min(-90).max(90).required(),
                maxlat: Joi.number().min(-90).max(90).required(),
                minlon: Joi.number().min(-180).max(180).required(),
                maxlon: Joi.number().min(-180).max(180).required()
            }).required()
        }).required()
    ).required()
});

module.exports = schema;
