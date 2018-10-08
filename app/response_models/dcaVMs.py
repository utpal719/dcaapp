def exponential_resp_model(**kwargs):

    input = kwargs.get("input", None)
    output = kwargs.get("output", None)
    datasource = kwargs.get("datasource", None)
    qi = kwargs.get("qi", None)
    mode = kwargs.get("mode", None)
    a = kwargs.get("a", None)
    pearsonr = kwargs.get("pearsonr", None)
    t = kwargs.get("t", None)
    tStep = kwargs.get("tStep", None)
    ref = kwargs.get("ref", None)
    wellName = kwargs.get("wellName", None)

    if(datasource is None):
        return {
            "output": output,
            "mode": mode,
            "ref": ref,
            "qi": qi,
            "a": a,
            "tSpan": t,
            "tStep": tStep
        }
    else:
        return {
            "output": output,
            "mode": mode,
            "ref": ref,
            "input": input,
            "datasource": datasource,
            "wellName": wellName,
            "qi": qi,
            "a": a,
            "pearsonr": pearsonr
        }


def harmonic_resp_model(**kwargs):

    input = kwargs.get("input", None)
    output = kwargs.get("output", None)
    datasource = kwargs.get("datasource", None)
    qi = kwargs.get("qi", None)
    mode = kwargs.get("mode", None)
    a = kwargs.get("a", None)
    pearsonr = kwargs.get("pearsonr", None)
    t = kwargs.get("t", None)
    tStep = kwargs.get("tStep", None)
    ref = kwargs.get("ref", None)
    wellName = kwargs.get("wellName", None)

    if(datasource is None):
        return {
            "output": output,
            "mode": mode,
            "ref": ref,
            "qi": qi,
            "a": a,
            "tSpan": t,
            "tStep": tStep
        }
    else:
        return {
            "output": output,
            "mode": mode,
            "ref": ref,
            "input": input,
            "datasource": datasource,
            "wellName": wellName,
            "qi": qi,
            "a": a,
            "pearsonr": pearsonr
        }


def hyperbolic_resp_model(**kwargs):

    input = kwargs.get("input", None)
    output = kwargs.get("output", None)
    datasource = kwargs.get("datasource", None)
    qi = kwargs.get("qi", None)
    mode = kwargs.get("mode", None)
    a = kwargs.get("a", None)
    pearsonr = kwargs.get("pearsonr", None)
    t = kwargs.get("t", None)
    n = kwargs.get("n", None)
    tStep = kwargs.get("tStep", None)
    ref = kwargs.get("ref", None)
    wellName = kwargs.get("wellName", None)

    if(datasource is None):
        return {
            "output": output,
            "mode": mode,
            "ref": ref,
            "qi": qi,
            "a": a,
            "tSpan": t,
            "n": n,
            "tStep": tStep
        }
    else:
        return {
            "output": output,
            "mode": mode,
            "ref": ref,
            "input": input,
            "datasource": datasource,
            "wellName": wellName,
            "qi": qi,
            "a": a,
            "n": n,
            "pearsonr": pearsonr
        }


def cumulative_resp_model(**kwargs):

    input = kwargs.get("input", None)
    output = kwargs.get("output", None)
    datasource = kwargs.get("datasource", None)
    mode = kwargs.get("mode", None)
    ref = kwargs.get("ref", None)
    wellName = kwargs.get("wellName", None)

    return {
        "output": output,
        "mode": mode,
        "ref": ref,
        "input": input,
        "datasource": datasource,
        "wellName": wellName
    }