/**
 * Neon HTTP Adapter for Better Auth
 * 
 * This adapter uses Neon's HTTP API instead of WebSocket/Pool
 * which is required for Hugging Face Spaces environment
 */

import { neon } from '@neondatabase/serverless';
import type { Adapter } from 'better-auth';

export function createNeonHttpAdapter(connectionString: string): Adapter {
  const sql = neon(connectionString);

  return {
    id: 'neon-http',
    
    async create({ model, data }) {
      const keys = Object.keys(data);
      const values = Object.values(data);
      const placeholders = keys.map((_, i) => `$${i + 1}`).join(', ');
      const columns = keys.join(', ');
      
      const query = `
        INSERT INTO ${model} (${columns})
        VALUES (${placeholders})
        RETURNING *
      `;
      
      const result = await sql(query, values);
      return result[0];
    },

    async findOne({ model, where }) {
      const whereKeys = Object.keys(where);
      const whereValues = Object.values(where);
      const whereClause = whereKeys.map((key, i) => `${key} = $${i + 1}`).join(' AND ');
      
      const query = `
        SELECT * FROM ${model}
        WHERE ${whereClause}
        LIMIT 1
      `;
      
      const result = await sql(query, whereValues);
      return result[0] || null;
    },

    async findMany({ model, where, limit, offset }) {
      let query = `SELECT * FROM ${model}`;
      const values: any[] = [];
      
      if (where && Object.keys(where).length > 0) {
        const whereKeys = Object.keys(where);
        const whereValues = Object.values(where);
        const whereClause = whereKeys.map((key, i) => `${key} = $${i + 1}`).join(' AND ');
        query += ` WHERE ${whereClause}`;
        values.push(...whereValues);
      }
      
      if (limit) {
        query += ` LIMIT ${limit}`;
      }
      
      if (offset) {
        query += ` OFFSET ${offset}`;
      }
      
      const result = await sql(query, values);
      return result;
    },

    async update({ model, where, data }) {
      const whereKeys = Object.keys(where);
      const whereValues = Object.values(where);
      const dataKeys = Object.keys(data);
      const dataValues = Object.values(data);
      
      const setClause = dataKeys.map((key, i) => `${key} = $${i + 1}`).join(', ');
      const whereClause = whereKeys.map((key, i) => `${key} = $${dataKeys.length + i + 1}`).join(' AND ');
      
      const query = `
        UPDATE ${model}
        SET ${setClause}
        WHERE ${whereClause}
        RETURNING *
      `;
      
      const result = await sql(query, [...dataValues, ...whereValues]);
      return result[0];
    },

    async delete({ model, where }) {
      const whereKeys = Object.keys(where);
      const whereValues = Object.values(where);
      const whereClause = whereKeys.map((key, i) => `${key} = $${i + 1}`).join(' AND ');
      
      const query = `
        DELETE FROM ${model}
        WHERE ${whereClause}
        RETURNING *
      `;
      
      const result = await sql(query, whereValues);
      return result[0];
    },
  };
}
