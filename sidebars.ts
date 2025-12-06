import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  bookSidebar: [
    {
      type: 'category',
      label: 'Part I: Foundations',
      items: ['01-intro', '02-tooling'],
    },
    {
      type: 'category',
      label: 'Part II: Building the Engine',
      items: ['03-init', '04-speckit', '05-cicd'],
    },
    {
      type: 'category',
      label: 'Part III: Authoring & Automation',
      items: ['06-writing', '07-diagrams', '08-validation'],
    },
    {
      type: 'category',
      label: 'Part IV: Publishing & Maintenance',
      items: ['09-deployment', '10-versioning'],
    },
  ],
};

export default sidebars;
