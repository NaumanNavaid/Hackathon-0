#!/usr/bin/env node
/**
 * Email MCP Server
 *
 * Model Context Protocol server for sending emails via Gmail API.
 *
 * Usage:
 *   1. Set GMAIL_CREDENTIALS_PATH environment variable
 *   2. Set GMAIL_TOKEN_PATH environment variable
 *   3. node index.js
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';

// Gmail scopes
const SCOPES = ['https://www.googleapis.com/auth/gmail.send'];

// Paths
const CREDENTIALS_PATH = process.env.GMAIL_CREDENTIALS_PATH ||
  path.join(process.env.HOME || process.env.USERPROFILE, '.gmail_credentials.json');
const TOKEN_PATH = process.env.GMAIL_TOKEN_PATH ||
  path.join(process.env.HOME || process.env.USERPROFILE, '.gmail_token.json');


/**
 * Authorize and get Gmail client
 */
async function getGmailClient() {
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH));
  const { client_secret, client_id, redirect_uris } = credentials.installed || credentials.web;

  const oAuth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    redirect_uris[0]
  );

  // Check if token exists
  if (fs.existsSync(TOKEN_PATH)) {
    const token = JSON.parse(fs.readFileSync(TOKEN_PATH));
    oAuth2Client.setCredentials(token);

    // Refresh if needed
    if (oAuth2Client.isTokenExpiring()) {
      const newToken = await oAuth2Client.refreshAccessToken();
      oAuth2Client.setCredentials(newToken.credentials);
      fs.writeFileSync(TOKEN_PATH, JSON.stringify(newToken.credentials));
    }
  }

  const gmail = google.gmail({ version: 'v1', auth: oAuth2Client });
  return gmail;
}


/**
 * Send email
 */
async function sendEmail({ to, subject, body, attachments = [] }) {
  try {
    const gmail = await getGmailClient();

    // Create email message
    let email = [
      `To: ${to}`,
      `Subject: ${subject}`,
      'Content-Type: text/plain; charset=utf-8',
      '',
      body
    ].join('\r\n');

    // Encode to base64url
    const encodedEmail = Buffer.from(email)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    // Send
    const result = await gmail.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: encodedEmail
      }
    });

    return {
      success: true,
      messageId: result.data.id,
      message: 'Email sent successfully'
    };

  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}


/**
 * Draft email (save, don't send)
 */
async function draftEmail({ to, subject, body }) {
  try {
    const gmail = await getGmailClient();

    let email = [
      `To: ${to}`,
      `Subject: ${subject}`,
      'Content-Type: text/plain; charset=utf-8',
      '',
      body
    ].join('\r\n');

    const encodedEmail = Buffer.from(email)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    const result = await gmail.users.drafts.create({
      userId: 'me',
      requestBody: {
        message: {
          raw: encodedEmail
          }
        }
    });

    return {
      success: true,
      draftId: result.data.id,
      message: 'Draft created successfully'
    };

  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}


// Create MCP server
const server = new Server(
  {
    name: 'email-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);


// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'send_email',
        description: 'Send an email via Gmail',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address'
            },
            subject: {
              type: 'string',
              description: 'Email subject'
            },
            body: {
              type: 'string',
              description: 'Email body (plain text)'
            }
          },
          required: ['to', 'subject', 'body']
        }
      },
      {
        name: 'draft_email',
        description: 'Create a draft email (does not send)',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address'
            },
            subject: {
              type: 'string',
              description: 'Email subject'
            },
            body: {
              type: 'string',
              description: 'Email body (plain text)'
            }
          },
          required: ['to', 'subject', 'body']
        }
      }
    ]
  };
});


// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'send_email':
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(await sendEmail(args), null, 2)
          }]
        };

      case 'draft_email':
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(await draftEmail(args), null, 2)
          }]
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: false,
          error: error.message
        }, null, 2)
      }],
      isError: true
    };
  }
});


// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  console.error('Email MCP Server running');
}

main().catch(console.error);
