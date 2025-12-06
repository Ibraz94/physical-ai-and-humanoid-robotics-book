import React from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';
import resources from '@site/data/resources.json';

type ResourceItem = {
  title: string;
  author: string;
  type: string;
  url: string;
  category: string;
  year: string;
};

function Resource({title, author, type, url, category, year}: ResourceItem) {
  return (
    <div className={clsx('col col--4 margin-bottom--md')}>
      <div className="card">
        <div className="card__header">
          <Heading as="h4">{title}</Heading>
          <span className="badge badge--secondary">{type}</span>
        </div>
        <div className="card__body">
          <p><strong>Author:</strong> {author}</p>
          <p><strong>Year:</strong> {year}</p>
          <p><strong>Category:</strong> {category}</p>
        </div>
        <div className="card__footer">
          <Link className="button button--secondary button--block" href={url}>
            View Resource
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function ResourceList(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <Heading as="h2" className="text--center margin-bottom--lg">
          Essential AI & Robotics Resources
        </Heading>
        <div className="row">
          {resources.map((props, idx) => (
            <Resource key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
