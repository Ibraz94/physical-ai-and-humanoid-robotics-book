import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';

type FeatureItem = {
  title: string;
  Svg?: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
  link: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Module 1: Foundations',
    description: (
      <>
        Master the basics of Physical AI and set up your ROS 2 Jazzy environment.
        Learn nodes, topics, and control theory code-first.
      </>
    ),
    link: '/docs/module-01/intro',
  },
  {
    title: 'Module 2: Isaac Sim',
    description: (
      <>
        Dive into high-fidelity simulation with NVIDIA Isaac Sim.
        Import URDFs, generate synthetic data, and train RL agents.
      </>
    ),
    link: '/docs/module-02/intro',
  },
  {
    title: 'Module 3: Gazebo',
    description: (
      <>
        Explore open-source simulation with Gazebo (Ignition).
        Build worlds, simulate sensors, and integrate Nav2.
      </>
    ),
    link: '/docs/module-03/intro',
  },
  {
    title: 'Module 4: Webots',
    description: (
      <>
        Prototype rapidly with Webots. Use the Supervisor API and
        cross-compile controllers for real hardware transfer.
      </>
    ),
    link: '/docs/module-04/intro',
  },
];

function Feature({title, Svg, description, link}: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <div className="text--center padding-horiz--md card">
        <div className="card__header">
           <Heading as="h3">{title}</Heading>
        </div>
        <div className="card__body">
          <p>{description}</p>
        </div>
        <div className="card__footer">
           <Link className="button button--primary button--block" to={link}>Start Module</Link>
        </div>
      </div>
    </div>
  );
}

export default function ModuleCards(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
