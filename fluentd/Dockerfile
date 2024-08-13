FROM fluent/fluentd:v1.17

USER root

# Install concat plugin
RUN gem install fluent-plugin-opensearch && \
    fluent-gem install fluent-plugin-concat

ENTRYPOINT ["tini",  "--", "/bin/entrypoint.sh"]
CMD ["fluentd"]