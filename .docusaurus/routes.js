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
    component: ComponentCreator('/hackathon-book/docs', 'b54'),
    routes: [
      {
        path: '/hackathon-book/docs',
        component: ComponentCreator('/hackathon-book/docs', 'b2a'),
        routes: [
          {
            path: '/hackathon-book/docs',
            component: ComponentCreator('/hackathon-book/docs', '426'),
            routes: [
              {
                path: '/hackathon-book/docs/01-intro',
                component: ComponentCreator('/hackathon-book/docs/01-intro', 'd72'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/02-tooling',
                component: ComponentCreator('/hackathon-book/docs/02-tooling', '93a'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/03-init',
                component: ComponentCreator('/hackathon-book/docs/03-init', '164'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/04-speckit',
                component: ComponentCreator('/hackathon-book/docs/04-speckit', '5c5'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/05-cicd',
                component: ComponentCreator('/hackathon-book/docs/05-cicd', '34e'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/06-writing',
                component: ComponentCreator('/hackathon-book/docs/06-writing', 'f0f'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/07-diagrams',
                component: ComponentCreator('/hackathon-book/docs/07-diagrams', 'cb6'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/08-validation',
                component: ComponentCreator('/hackathon-book/docs/08-validation', '65b'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/09-deployment',
                component: ComponentCreator('/hackathon-book/docs/09-deployment', '8c0'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/10-versioning',
                component: ComponentCreator('/hackathon-book/docs/10-versioning', 'acc'),
                exact: true
              },
              {
                path: '/hackathon-book/docs/module-01-foundations/control-theory',
                component: ComponentCreator('/hackathon-book/docs/module-01-foundations/control-theory', '812'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/hackathon-book/docs/module-01-foundations/nodes-topics',
                component: ComponentCreator('/hackathon-book/docs/module-01-foundations/nodes-topics', '8be'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/hackathon-book/docs/module-01-foundations/setup-ros2',
                component: ComponentCreator('/hackathon-book/docs/module-01-foundations/setup-ros2', 'd42'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/hackathon-book/docs/module-01/intro',
                component: ComponentCreator('/hackathon-book/docs/module-01/intro', '7fc'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/hackathon-book/docs/module-02/intro',
                component: ComponentCreator('/hackathon-book/docs/module-02/intro', '2ad'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/hackathon-book/docs/module-03/intro',
                component: ComponentCreator('/hackathon-book/docs/module-03/intro', 'f92'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/hackathon-book/docs/module-04/intro',
                component: ComponentCreator('/hackathon-book/docs/module-04/intro', '30d'),
                exact: true,
                sidebar: "courseSidebar"
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
