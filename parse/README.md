mvn clean compile assembly:single

cat sentences.txt | java -d64 -server -Xms25G -Xmx25G \
 -jar ./target/parse-1-jar-with-dependencies.jar
