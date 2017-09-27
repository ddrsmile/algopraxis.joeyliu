package utils.inputparser;
import java.lang.reflect.Constructor;

public class ParserFactory<E> {
    Class<E> type;

    public ParserFactory(Class<E> type) {
        this.type = type;
    }

    @SuppressWarnings("unchecked")
    public <E> E create(String inputPath) {
        E parser;
        try {
            Constructor ctor = type.getConstructor(String.class);
            parser = (E) ctor.newInstance(inputPath);
        } catch (Throwable e) {
            System.err.println(e);
            parser = null;
        }
        return parser;
    }
}