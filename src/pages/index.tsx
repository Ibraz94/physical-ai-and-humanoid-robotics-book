import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import ModuleCards from '@site/src/components/Homepage/ModuleCards';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={styles.heroBanner}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          Physical AI & Humanoid Robotics
        </Heading>
        <p className="hero__subtitle">
          Master Embodied Intelligence with ROS 2, Isaac Sim, Gazebo, and Webots.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/module-01/intro">
            Start Learning 🚀
          </Link>
        </div>
      </div>
    </header>
  );
}

import ResourceList from '@site/src/components/Homepage/ResourceList';

// ... existing imports

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Course: ${siteConfig.title}`}
      description="A code-driven course on Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <ModuleCards />
        <div className="container">
          <hr className="margin-vert--lg" style={{borderColor: 'var(--ifm-color-primary-dark)'}} />
        </div>
        <ResourceList />
      </main>
    </Layout>
  );
}