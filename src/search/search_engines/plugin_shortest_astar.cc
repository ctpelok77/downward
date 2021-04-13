#include "shortest_eager_search.h"
#include "eager_search.h"

#include "search_common.h"

#include "../option_parser.h"
#include "../plugin.h"

using namespace std;

namespace plugin_shortest_astar {
static shared_ptr<SearchEngine> _parse(OptionParser &parser) {
    parser.document_synopsis(
        "A* search (eager)",
        "A* is a special case of eager best first search that uses g+h "
        "as f-function. "
        "Second, g evaluator based on unit costs is used to break ties. "
        "Last, we break ties using the h evaluator. Closed nodes are re-opened.");
    parser.document_note(
        "lazy_evaluator",
        "When a state s is taken out of the open list, the lazy evaluator h "
        "re-evaluates s. If h(s) changes (for example because h is path-dependent), "
        "s is not expanded, but instead reinserted into the open list. "
        "This option is currently only present for the A* algorithm.");
    parser.document_note(
        "Equivalent statements using general eager search",
        "\n```\n--search myastar(evaluator)\n```\n"
        "is equivalent to\n"
        "```\n--evaluator d=prototype_g(transform=adapt_costs(cost_type=one))\n"
        "```\n--evaluator h=evaluator\n"
        "--search eager(tiebreaking([sum([g(), h]), d, h], unsafe_pruning=false),\n"
        "               reopen_closed=true, f_eval=sum([g(), h]))\n"
        "```\n", true);
    parser.add_option<shared_ptr<Evaluator>>("eval", "evaluator for h-value");
    parser.add_option<shared_ptr<Evaluator>>(
        "lazy_evaluator",
        "An evaluator that re-evaluates a state before it is expanded.",
        OptionParser::NONE);

    eager_search::add_options_to_parser(parser);
    Options opts = parser.parse();

    shared_ptr<eager_search::ShortestEagerSearch> engine;
    if (!parser.dry_run()) {
        auto temp = search_common::create_shortest_astar_open_list_factory_and_f_eval(opts);
        opts.set("open", temp.first);
        opts.set("f_eval", temp.second[0]);
        opts.set("d_eval", temp.second[1]);
        opts.set("reopen_closed", true);
        vector<shared_ptr<Evaluator>> preferred_list;
        opts.set("preferred", preferred_list);
        engine = make_shared<eager_search::ShortestEagerSearch>(opts);
    }

    return engine;
}

static Plugin<SearchEngine> _plugin("shortest_astar", _parse);
}