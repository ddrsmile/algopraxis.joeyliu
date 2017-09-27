package utils.inputparser;

public abstract class AbstractParserFactory<S,T> {
    public abstract IParser<S,T> create();
    public abstract IParser<S,T> create(String inputPath);
}