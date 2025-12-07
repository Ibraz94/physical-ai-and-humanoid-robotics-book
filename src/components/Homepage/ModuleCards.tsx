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
    title: 'Module 1: Foundation & ROS 2',
    description: (
      <>
        Master the basics of Physical AI, ROS 2 Jazzy setup, nodes, topics, and core control principles.
      </>
    ),
    link: '/docs/module-01/intro',
  },
  {
    title: 'Module 2: Gazebo',
    description: (
      <>
        Build simulation worlds, test sensors, run Nav2, and prototype interactive environments using Unity.
      </>
    ),
    link: '/docs/module-02/intro',
  },
  {
    title: 'Module 3: NVIDIA Isaac',
    description: (
      <>
        Use Isaac Sim for high-fidelity robotics simulation, URDF import, synthetic data generation, and RL training.
      </>
    ),
    link: '/docs/module-03/intro',
  },
  {
    title: 'Module 4: VLA',
    description: (
      <>
        Explore multimodal robotics with VLA models that connect perception & language understanding.
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
