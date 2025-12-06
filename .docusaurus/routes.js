import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/hackathon-book/__docusaurus/debug',
    component: ComponentCreator('/hackathon-book/__docusaurus/debug', 'c29'),
    exact: true
  },
  {
    path: '/hackathon-book/__docusaurus/debug/config',
    component: ComponentCreator('/hackathon-book/__docusaurus/debug/config', 'ead'),
    exact: true
  },
  {
    path: '/hackathon-book/__docusaurus/debug/content',
    component: ComponentCreator('/hackathon-book/__docusaurus/debug/content', '336'),
    exact: true
  },
  {
    path: '/hackathon-book/__docusaurus/debug/globalData',
    component: ComponentCreator('/hackathon-book/__docusaurus/debug/globalData', 'bb6'),
    exact: true
  },
  {
    path: '/hackathon-book/__docusaurus/debug/metadata',
    component: ComponentCreator('/hackathon-book/__docusaurus/debug/metadata', '644'),
    exact: true
  },
  {
    path: '/hackathon-book/__docusaurus/debug/registry',
    component: ComponentCreator('/hackathon-book/__docusaurus/debug/registry', 'e50'),
    exact: true
  },
  {
    path: '/hackathon-book/__docusaurus/debug/routes',
    component: ComponentCreator('/hackathon-book/__docusaurus/debug/routes', 'e1b'),
    exact: true
  },
  {
    path: '/hackathon-book/docs',
    component: ComponentCreator('/hackathon-book/docs', '2c7'),
    routes: [
      {
        path: '/hackathon-book/docs',
        component: ComponentCreator('/hackathon-book/docs', '233'),
        routes: [
          {
            path: '/hackathon-book/docs',
            component: ComponentCreator('/hackathon-book/docs', 'f13'),
            routes: [
              {
                path: '/hackathon-book/docs/01-intro',
                component: ComponentCreator('/hackathon-book/docs/01-intro', '304'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/02-tooling',
                component: ComponentCreator('/hackathon-book/docs/02-tooling', '030'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/03-init',
                component: ComponentCreator('/hackathon-book/docs/03-init', '456'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/04-speckit',
                component: ComponentCreator('/hackathon-book/docs/04-speckit', '4b0'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/05-cicd',
                component: ComponentCreator('/hackathon-book/docs/05-cicd', 'e45'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/06-writing',
                component: ComponentCreator('/hackathon-book/docs/06-writing', '354'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/07-diagrams',
                component: ComponentCreator('/hackathon-book/docs/07-diagrams', '671'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/08-validation',
                component: ComponentCreator('/hackathon-book/docs/08-validation', '11d'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/09-deployment',
                component: ComponentCreator('/hackathon-book/docs/09-deployment', 'cd5'),
                exact: true,
                sidebar: "bookSidebar"
              },
              {
                path: '/hackathon-book/docs/10-versioning',
                component: ComponentCreator('/hackathon-book/docs/10-versioning', '0b0'),
                exact: true,
                sidebar: "bookSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/hackathon-book/',
    component: ComponentCreator('/hackathon-book/', '32a'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
