import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/physical-ai-and-humanoid-robotics-book/__docusaurus/debug',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/__docusaurus/debug', 'd5f'),
    exact: true
  },
  {
    path: '/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/config',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/config', 'add'),
    exact: true
  },
  {
    path: '/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/content',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/content', '35a'),
    exact: true
  },
  {
    path: '/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/globalData',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/globalData', 'c72'),
    exact: true
  },
  {
    path: '/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/metadata',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/metadata', '98a'),
    exact: true
  },
  {
    path: '/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/registry',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/registry', '39b'),
    exact: true
  },
  {
    path: '/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/routes',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/__docusaurus/debug/routes', '290'),
    exact: true
  },
  {
    path: '/physical-ai-and-humanoid-robotics-book/docs',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs', '905'),
    routes: [
      {
        path: '/physical-ai-and-humanoid-robotics-book/docs',
        component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs', 'af0'),
        routes: [
          {
            path: '/physical-ai-and-humanoid-robotics-book/docs',
            component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs', 'd4d'),
            routes: [
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/02-tooling',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/02-tooling', 'ff7'),
                exact: true
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/04-speckit',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/04-speckit', '0a9'),
                exact: true
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/05-cicd',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/05-cicd', 'fb7'),
                exact: true
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/06-writing',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/06-writing', '1e8'),
                exact: true
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/07-diagrams',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/07-diagrams', 'fc9'),
                exact: true
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/08-validation',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/08-validation', 'cf8'),
                exact: true
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/09-deployment',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/09-deployment', '771'),
                exact: true
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/10-versioning',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/10-versioning', 'a5e'),
                exact: true
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/conclusion',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/conclusion', '2a3'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/intro',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/intro', '9ea'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/ai-agents',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/ai-agents', '059'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/best-practices',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/best-practices', '248'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/control-theory',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/control-theory', '760'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/key-takeways',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/key-takeways', 'a9a'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/nodes-topics',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/nodes-topics', '754'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/service-action',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/service-action', 'ae5'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/setup-ros2',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/setup-ros2', 'eae'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/urdf',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01-foundations/urdf', '877'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-01/intro',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-01/intro', 'd49'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-02/generating-synthetic',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-02/generating-synthetic', 'e2f'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-02/intro',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-02/intro', 'f92'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-02/mastering-gazebo-simulation',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-02/mastering-gazebo-simulation', '09b'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-02/module-summary',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-02/module-summary', '75b'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-02/physics-simulation',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-02/physics-simulation', '9b2'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-02/sim-to-real-transfer',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-02/sim-to-real-transfer', 'ba4'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-02/unity-for-photorealistic',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-02/unity-for-photorealistic', 'b95'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-03/autonomous-navigation',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-03/autonomous-navigation', 'e57'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-03/building-isaac',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-03/building-isaac', '34b'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-03/deploying',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-03/deploying', '43a'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-03/installing-Isaac',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-03/installing-Isaac', 'd5f'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-03/intro',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-03/intro', '2db'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-03/isaac-ros',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-03/isaac-ros', 'b32'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-03/summary',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-03/summary', '50c'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-04/capstone-project',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-04/capstone-project', '014'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-04/cognitive-planning',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-04/cognitive-planning', '571'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-04/intro',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-04/intro', 'c4d'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-04/multi-modal',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-04/multi-modal', '712'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-04/summary',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-04/summary', 'cfe'),
                exact: true,
                sidebar: "courseSidebar"
              },
              {
                path: '/physical-ai-and-humanoid-robotics-book/docs/module-04/voice-to-action',
                component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/docs/module-04/voice-to-action', '561'),
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
    path: '/physical-ai-and-humanoid-robotics-book/',
    component: ComponentCreator('/physical-ai-and-humanoid-robotics-book/', 'f1c'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
